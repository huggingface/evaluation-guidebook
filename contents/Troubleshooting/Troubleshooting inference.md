## My model is very slow!
### Changing the batch size
If you want absolute reproducibility (given a specific hardware and a specific evaluation prompt), you're probably using a batch size of one. However, moving to higher batch sizes will likely make your evaluation faster (given that it fits within the memory requirements of your hardware)

### Data parallelism
You can also duplicate your model on several GPUs instead of loading it on one single GPU, and provide subsets of the data to each GPU copy, then aggregate the computation results. 
This means that each data stream will be handled in parallel, at the same time as the others, which divides your total execution time by the number of GPUs. 
However, if you can, all GPUs should be on a single node to avoid inter-node bottlenecks.

### Changing the inference code
Not all inference libraries run at the same speed, and some code is more optimized than other. You'll need to experiment a bit to find which libraries have the fastest inference, and if you are using pytorch, I recommend looking at the model inference optimization checklist [here](https://pytorch.org/serve/performance_checklist.html).

### Changing the precision
If your model is very slow, you can reduce its size by reducing the precision of the computations. A model stored in float32 does very precise computations (using 32bits per number stored!) that are also very memory and compute heavy - moving to `blfoat16` or `float16` (half the precision) should make the model twice as fast at a loss of precision which should almost not matter. If you want bumps in speed, you can quantize it even more, to 8 or 4 bits (using `gptq` or `bitsandbytes` for example). - 

## My model is very big!
### Estimating memory requirements
You can estimate the minimal theoretical memory required to load a given model (and therefore hardware) with the **following formula**:

`<memory (in GB)> = <number of parameters (in G)> * <precision factor>`

Since you can store 8 bits in a Byte, the memory required is the total number of parameters times the number of Bytes required to store one parameter. The precision factor is therefore 4 for `float32`,  2 for `float16` or `bfoat16`, 1 for `8bit`, and 0.5 for `4bit` models, etc.

And that's it! 

I would actually recommend using  `<memory (in GB)> = <number of parameters (in G)> * (<precision factor> * 110%)`, to be on the safer side, as inference will require a bit more memory than just loading the model (you'll also need to load the batches).

### What should you do if your model does not fit on a GPU?
#### Quantization
The first obvious thing is to play on the `<precision factor>` above: going from float32 to 4 bits reduces memory requirements by 8! 
However, using too low a precision can give worse results, so for some models (especially medium range), you might want to stay in float16 or 8bit. (Quantization seems to affect very big models performance less, possibly because of information redundancy).
#### Model parallelism
Model parallelism includes a range of techniques which cut your model in smaller sub-model pieces, to load and run each of these smaller pieces on a single different GPU. This requires less memory since you never load the full model at once, but can be slower.

The 2 main types of model parallelism are
- Pipeline parallelism, where the model is split at the whole layer level, and the layers are dispatched on different GPUs. Since layer 1's output is layer 2's input, this leads to a slower execution, as GPUs will be idle while waiting, which is called a "bubble" (and data must be transferred from one GPU to the next). The bubble can be reduced by splitting the inputs into smaller batches. It's being natively added to PyTorch with the `PiPPy` [lib](https://github.com/pytorch/PiPPy), and this is what `accelerate` uses under the hood for parallelism.
- Tensor parallelism, where the model is split at the matrix computation level. This means that the matrices will be split on rows or columns, and the total result aggregated. This is incredibly efficient as long as all GPUs are on the same node (to avoid inter node network bottlenecks), but can be hard to code. You'll find cool implementations of this in the `vllm` lib. It provides **insane speedups**.

The best document on the different kinds of parallelism (including data parallelism, for speedups) is [here](https://huggingface.co/docs/transformers/v4.15.0/en/parallelism).

#### CPU offloading
CPU offloading moves some of the computations and models parts to CPU, in order to reduce GPU memory usage. It's **considerably slower** than any other method here, mostly because you need to move data from one device to another all the time.

An example of this is [ZeRO-Offload](https://arxiv.org/abs/2101.06840) by Deepspeed, which distributes parameters between CPU and GPU (on top of using other optimization described in the ZeRO-2 paper). On CPU are passed gradients, optimizer states and fp32 model parameter computations during optimisation, whereas on GPU, you'll find fp16 parameters and forward/backward pass, to leverage CPU memory used and GPU computations while minimizing communication between both.

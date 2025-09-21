# LaTeX로 수학 능력 평가하기

LaTeX 구문 분석은 어렵습니다. 이는 출력으로 $\LaTeX$를 예상하는 모델을 평가할 때 문제가 됩니다. [MATH 벤치마크](https://huggingface.co/datasets/lighteval/MATH)의 경우가 이에 해당합니다.

이 벤치마크는 수학적 계산과 기호를 표현하기 위해 $\LaTeX$를 사용합니다. 이 작업을 평가하는 것은 정답과 모델 출력을 구문 분석하고 비교하는 문제여야 합니다.  
그런데 $\LaTeX$를 구문 분석하는 올바른 방법이 없다는 것이 밝혀졌습니다:


![](../../assets/sympy_doc.png)  
*[`sympy`](https://github.com/sympy/sympy) 문서에서*

lm-evaluation harness는 LaTeX를 구문 분석하고 표현식을 비교하기 위해 [`sympy`](https://github.com/sympy/sympy)(기호 수학을 위한 Python 라이브러리)를 사용합니다.  
`sympy`를 사용하여 정답을 구문 분석하려고 할 때(정답을 자기 자신과 비교), 우리는 약 0.94의 정확도만 얻습니다.
어떻게 그럴 수 있을까요? 알고 보니 `sympy`는 특정(올바른 $\LaTeX$) 표현식을 구문 분석할 수 없습니다.

예를 들면: 

```
couldn't parse one of [0,1) or [0,1), I expected one of these: ']'
[0,1)
~~^
```

```
couldn't parse one of (-\iny,-5]\cup[5,\iny) or (-\iny,-5]\cup[5,\iny), I expected something else here
(-\iny,-5]\cup[5,\iny)
~~~~~~^
```

```
couldn't parse one of -\frac{1}{{}2x} or -\frac{1}{{}2x}, I don't understand this
-\frac{1}{{}2x}
~~~~~~~~~~~^
```

### 이 문제를 어떻게 해결할 수 있을까요?

$\LaTeX$ [문법](https://github.com/sympy/sympy/blob/master/sympy/parsing/latex/lark/grammar/latex.lark)을 다시 작성하고, 필요한 기능을 코드에 추가하거나, 모델 점수를 개선하기 위해 코드에 수동 검사를 추가할 수 있습니다. 깊은 토끼 굴에 빠질 뻔한 후, 우리는 코드에 문자열 비교 검사를 추가하는 것이 충분하다고 결정했습니다.

![LM Eval Harness에 대한 수정](../../assets/lm_eval_diff.png)  
*LM Evaluation Harness에 대한 수정*

### 결과

다음은 처음 25개 모델의 이전 결과와 새로운 결과를 비교한 표입니다.

<div id="xdihwljbql" style="padding-left:0px;padding-right:0px;padding-top:10px;padding-bottom:10px;overflow-x:auto;overflow-y:auto;width:auto;height:auto;">
<table class="gt_table" data-quarto-disable-processing="false" data-quarto-bootstrap="false">
<thead>
  <tr class="gt_heading">
    <td colspan="5" class="gt_heading gt_title gt_font_normal">MATH 벤치마크에서 원래 구문 분석기와 수정된 구문 분석기 비교</td>
  </tr>
<tr class="gt_col_headings gt_spanner_row">
  <th class="gt_col_heading gt_columns_bottom_border gt_left" rowspan="2" colspan="1" scope="col" id="Model">모델</th>
  <th class="gt_center gt_columns_top_border gt_column_spanner_outer" rowspan="1" colspan="2" scope="colgroup" id="Score">
    <span class="gt_column_spanner">점수</span>
  </th>
  <th class="gt_center gt_columns_top_border gt_column_spanner_outer" rowspan="1" colspan="2" scope="colgroup" id="Rank">
    <span class="gt_column_spanner">순위</span>
  </th>
</tr>
<tr class="gt_col_headings">
  <th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1" scope="col" id="Original">원본</th>
  <th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1" scope="col" id="Fixed parser">수정된 구문 분석기</th>
  <th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1" scope="col" id="Original">원본</th>
  <th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1" scope="col" id="Fixed parser">수정된 구문 분석기</th>
</tr>
</thead>
<tbody class="gt_table_body">
  <tr>
    <td class="gt_row gt_left">rombodawg/Rombos-LLM-V2.5-Qwen-72b</td>
    <td class="gt_row gt_right">47.58</td>
    <td class="gt_row gt_right">50.68</td>
    <td style="color: #FFFFFF; background-color: #000000;" class="gt_row gt_right">1</td>
    <td style="color: #FFFFFF; background-color: #000000;" class="gt_row gt_right">1</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">MaziyarPanahi/calme-2.2-qwen2-72b</td>
    <td class="gt_row gt_right">41.16</td>
    <td class="gt_row gt_right">43.43</td>
    <td style="color: #FFFFFF; background-color: #41181f;" class="gt_row gt_right">2</td>
    <td style="color: #FFFFFF; background-color: #41181f;" class="gt_row gt_right">2</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">arcee-ai/Arcee-Nova</td>
    <td class="gt_row gt_right">40.48</td>
    <td class="gt_row gt_right">42.90</td>
    <td style="color: #FFFFFF; background-color: #82303e;" class="gt_row gt_right">3</td>
    <td style="color: #FFFFFF; background-color: #82303e;" class="gt_row gt_right">3</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">fblgit/TheBeagle-v2beta-32B-MGS</td>
    <td class="gt_row gt_right">39.43</td>
    <td class="gt_row gt_right">42.52</td>
    <td style="color: #FFFFFF; background-color: #c3495e;" class="gt_row gt_right">4</td>
    <td style="color: #FFFFFF; background-color: #c3495e;" class="gt_row gt_right">4</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">rombodawg/Rombos-LLM-V2.5-Qwen-32b</td>
    <td class="gt_row gt_right">39.12</td>
    <td class="gt_row gt_right">41.99</td>
    <td style="color: #000000; background-color: #ca6866;" class="gt_row gt_right">5</td>
    <td style="color: #000000; background-color: #ca6866;" class="gt_row gt_right">5</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">dnhkng/RYS-XLarge</td>
    <td class="gt_row gt_right">38.97</td>
    <td class="gt_row gt_right">41.24</td>
    <td style="color: #000000; background-color: #a58c5e;" class="gt_row gt_right">6</td>
    <td style="color: #000000; background-color: #a58c5e;" class="gt_row gt_right">6</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">dfurman/CalmeRys-78B-Orpo-v0.1</td>
    <td class="gt_row gt_right">37.92</td>
    <td class="gt_row gt_right">40.71</td>
    <td style="color: #000000; background-color: #6ec352;" class="gt_row gt_right">8</td>
    <td style="color: #000000; background-color: #80b156;" class="gt_row gt_right">7</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">MaziyarPanahi/calme-2.2-rys-78b</td>
    <td class="gt_row gt_right">37.92</td>
    <td class="gt_row gt_right">39.95</td>
    <td style="color: #000000; background-color: #6ec352;" class="gt_row gt_right">8</td>
    <td style="color: #000000; background-color: #4cbd81;" class="gt_row gt_right">9</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">MaziyarPanahi/calme-2.4-rys-78b</td>
    <td class="gt_row gt_right">37.69</td>
    <td class="gt_row gt_right">40.41</td>
    <td style="color: #000000; background-color: #4cbd81;" class="gt_row gt_right">9</td>
    <td style="color: #000000; background-color: #5ece55;" class="gt_row gt_right">8</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">MaziyarPanahi/calme-2.3-rys-78b</td>
    <td class="gt_row gt_right">36.56</td>
    <td class="gt_row gt_right">38.97</td>
    <td style="color: #000000; background-color: #3aacad;" class="gt_row gt_right">10</td>
    <td style="color: #000000; background-color: #3aacad;" class="gt_row gt_right">10</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">MaziyarPanahi/calme-2.1-rys-78b</td>
    <td class="gt_row gt_right">36.40</td>
    <td class="gt_row gt_right">38.90</td>
    <td style="color: #000000; background-color: #279cd9;" class="gt_row gt_right">11</td>
    <td style="color: #000000; background-color: #279cd9;" class="gt_row gt_right">11</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">Qwen/Qwen2.5-72B</td>
    <td class="gt_row gt_right">36.10</td>
    <td class="gt_row gt_right">38.67</td>
    <td style="color: #000000; background-color: #23a7e6;" class="gt_row gt_right">12</td>
    <td style="color: #000000; background-color: #23a7e6;" class="gt_row gt_right">12</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">MaziyarPanahi/calme-2.1-qwen2-72b</td>
    <td class="gt_row gt_right">36.03</td>
    <td class="gt_row gt_right">38.07</td>
    <td style="color: #000000; background-color: #25bce6;" class="gt_row gt_right">13</td>
    <td style="color: #000000; background-color: #36d0e2;" class="gt_row gt_right">15</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">Qwen/Qwen2-Math-72B-Instruct</td>
    <td class="gt_row gt_right">35.95</td>
    <td class="gt_row gt_right">38.14</td>
    <td style="color: #000000; background-color: #27d2e5;" class="gt_row gt_right">14</td>
    <td style="color: #000000; background-color: #27d2e5;" class="gt_row gt_right">14</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">dfurman/Qwen2-72B-Orpo-v0.1</td>
    <td class="gt_row gt_right">35.42</td>
    <td class="gt_row gt_right">38.14</td>
    <td style="color: #000000; background-color: #36d0e2;" class="gt_row gt_right">15</td>
    <td style="color: #000000; background-color: #25bce6;" class="gt_row gt_right">13</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">abacusai/Smaug-Qwen2-72B-Instruct</td>
    <td class="gt_row gt_right">35.35</td>
    <td class="gt_row gt_right">37.46</td>
    <td style="color: #000000; background-color: #6691d6;" class="gt_row gt_right">16</td>
    <td style="color: #000000; background-color: #d73a91;" class="gt_row gt_right">19</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">anthracite-org/magnum-v1-72b</td>
    <td class="gt_row gt_right">35.27</td>
    <td class="gt_row gt_right">37.69</td>
    <td style="color: #FFFFFF; background-color: #ae33c4;" class="gt_row gt_right">18</td>
    <td style="color: #000000; background-color: #7e72d0;" class="gt_row gt_right">16</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">alpindale/magnum-72b-v1</td>
    <td class="gt_row gt_right">35.27</td>
    <td class="gt_row gt_right">37.69</td>
    <td style="color: #FFFFFF; background-color: #ae33c4;" class="gt_row gt_right">18</td>
    <td style="color: #000000; background-color: #7e72d0;" class="gt_row gt_right">16</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">Qwen/Qwen2-72B-Instruct</td>
    <td class="gt_row gt_right">35.12</td>
    <td class="gt_row gt_right">37.69</td>
    <td style="color: #000000; background-color: #d73a91;" class="gt_row gt_right">19</td>
    <td style="color: #FFFFFF; background-color: #c614be;" class="gt_row gt_right">18</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">dnhkng/RYS-XLarge-base</td>
    <td class="gt_row gt_right">34.67</td>
    <td class="gt_row gt_right">37.16</td>
    <td style="color: #000000; background-color: #e3715f;" class="gt_row gt_right">20</td>
    <td style="color: #000000; background-color: #e3715f;" class="gt_row gt_right">20</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">Undi95/MG-FinalMix-72B</td>
    <td class="gt_row gt_right">33.61</td>
    <td class="gt_row gt_right">36.10</td>
    <td style="color: #000000; background-color: #f4c314;" class="gt_row gt_right">22</td>
    <td style="color: #000000; background-color: #eea82d;" class="gt_row gt_right">21</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">abacusai/Dracarys-72B-Instruct</td>
    <td class="gt_row gt_right">33.61</td>
    <td class="gt_row gt_right">35.65</td>
    <td style="color: #000000; background-color: #f4c314;" class="gt_row gt_right">22</td>
    <td style="color: #000000; background-color: #eac222;" class="gt_row gt_right">22</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">Qwen/Qwen2.5-32B</td>
    <td class="gt_row gt_right">32.85</td>
    <td class="gt_row gt_right">35.50</td>
    <td style="color: #000000; background-color: #d1b64b;" class="gt_row gt_right">23</td>
    <td style="color: #000000; background-color: #d1b64b;" class="gt_row gt_right">23</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">anthracite-org/magnum-v2-72b</td>
    <td class="gt_row gt_right">31.65</td>
    <td class="gt_row gt_right">34.06</td>
    <td style="color: #000000; background-color: #b7aa75;" class="gt_row gt_right">24</td>
    <td style="color: #000000; background-color: #b7aa75;" class="gt_row gt_right">24</td>
  </tr>
  <tr>
    <td class="gt_row gt_left">dnhkng/RYS-Huge-bnb-4bit</td>
    <td class="gt_row gt_right">31.57</td>
    <td class="gt_row gt_right">33.84</td>
    <td style="color: #000000; background-color: #9e9e9e;" class="gt_row gt_right">25</td>
    <td style="color: #000000; background-color: #9e9e9e;" class="gt_row gt_right">25</td>
  </tr>
</tbody>
</table>
</div>
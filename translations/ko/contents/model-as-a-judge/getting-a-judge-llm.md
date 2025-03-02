# 평가 LLM 선택하기

기존 LLM을 사용할 때, [범용적이고 높은 능력을 가진 모델](https://arxiv.org/abs/2306.05685v4), 선호도 데이터를 구별하도록 특별히 훈련된 [작은 전문 모델](https://arxiv.org/abs/2405.01535)을 사용하거나, 직접 자신의 모델을 훈련할 수 있습니다.

## 범용 LLM 사용하기

더 뛰어난 LLM(예: ChatGPT)의 등장으로, 일부 연구자들은 큰 모델을 평가자로 사용하는 방법을 탐구하기 시작했습니다. 현재 가장 우수한 대형 모델 평가자는 주로 비공개 소스 모델(Claude나 gpt-o 모델과 같은)이지만, [Qwen 2.5](https://huggingface.co/collections/Qwen/qwen25-66e81a666513e518adb90d9e), [Command R+](https://huggingface.co/CohereForAI/c4ai-command-r-plus-08-2024), [Llama 3.1-405-Instruct](meta-llama/Llama-3.1-405B-Instruct)와 같은 고품질 모델 덕분에 오픈 소스와의 격차가 매우 빠르게 좁혀지고 있습니다.

비공개 소스 모델은 우수한 성능에도 불구하고 다음과 같은 여러 단점이 있습니다:
- API를 통해 제공되므로, 모델(따라서 결과)이 예고 없이 변경될 수 있어 평가의 재현성을 해칠 수 있습니다.
- 블랙박스로, 해석이 불가능합니다.
- 데이터 유출/데이터 개인정보 부족의 가능한 원인으로, 인터넷을 통해 제3자에게 데이터를 전송하며(로컬에서 관리되는 데이터보다 안전성이 떨어짐), 데이터가 어떻게 처리되는지 확실히 알 수 없습니다(종종 훈련 세트에 사용되는 것을 거부해야 함).

그러나, 이러한 모델은 로컬 설정이나 하드웨어 접근 없이도 누구나 고품질 모델에 접근할 수 있게 해줍니다. 이러한 장점은 이제 대부분의 고품질 오픈 모델에도 존재하며, 모델 제공업체를 통해 접근 가능하고 위의 첫 두 가지 문제를 해결합니다.

모델 제공업체를 선택하는 데 도움이 필요하면 [여기](https://huggingface.co/spaces/ArtificialAnalysis/LLM-Performance-Leaderboard)에서 좋은 비용 분석을 찾을 수 있습니다.

## 작은 전문 LLM 평가 모델 사용하기

작은 전문 LLM 평가자를 사용하는 선택을 할 수도 있습니다. 종종 몇 십억 개의 매개변수만으로, 대부분의 최신 소비자 하드웨어에서 로컬로 실행할 수 있으며, 처음부터 학습하거나 지시 데이터를 사용해 미세 조정할 수 있습니다. 일반적으로 특정 프롬프트 형식을 따라야 합니다.

일부 기존 모델:
- Flow-Judge-v0.1 ([가중치](https://huggingface.co/collections/flowaicom/flow-judge-v01-66e6af5fc3b3a128bde07dec)), 3.8B 매개변수, 합성 선호도 데이터셋으로 미세 조정된 Phi-3.5-mini-instruct 모델
- Prometheus ([가중치](https://huggingface.co/prometheus-eval/prometheus-13b-v1.0), [논문](https://arxiv.org/abs/2310.08491)), 13B 매개변수, 합성 선호도 데이터셋에서 처음부터 학습된 모델. 더 큰 합성 선호도 데이터셋에서 미세 조정된 Mistral-7B-Instruct-v0.2인 7B 매개변수의 [v2](https://huggingface.co/prometheus-eval/prometheus-7b-v2.0)도 있으며, 가중치 병합이 추가됨
- JudgeLM ([논문](https://arxiv.org/abs/2310.17631)), 7B에서 33B 매개변수, 다양한 모델로 생성된 합성 선호도 데이터셋에서 처음부터 학습된 모델.

## 자신의 모델 훈련하기
자신만의 평가자 LLM을 훈련하거나 미세 조정하기로 선택할 수도 있습니다.

먼저 관심 있는 작업에 대한 선호도 데이터를 수집해야 합니다. 이 데이터는 다음에서 얻을 수 있습니다:
- 기존 [인간 선호도 데이터셋](https://www.kaggle.com/competitions/lmsys-chatbot-arena)
- 모델이 생성한 선호도 데이터(위의 작은 모델 평가자 논문의 데이터 섹션을 따라 직접 생성하거나, Prometheus의 [선호도](https://huggingface.co/datasets/prometheus-eval/Preference-Collection) 및 [피드백](https://huggingface.co/datasets/prometheus-eval/Feedback-Collection) 컬렉션과 같은 곳에서 직접 얻을 수 있음).

그런 다음 처음부터 훈련할 작은 모델을 사용할지, 아니면 다음과 같이 할 수 있는 기존 모델을 사용할지 결정해야 합니다:
- 새로운 더 작은 모델로 증류
- 양자화
- 그런 다음 위의 데이터를 사용하여 미세 조정(모델이 크고 훈련 컴퓨팅 능력이 낮은 경우 peft 또는 어댑터 가중치 사용)
	- 명백히 [지시 모델보다 보상 모델에서 시작하는 것이 더 효과적](https://x.com/dk21/status/1826292289930674590)입니다.
# LLM 평가 가이드북 ⚖️

특정 작업에서 LLM이 얼마나 잘 수행하는지 확인하는 방법이 궁금하셨다면, 이 가이드가 도움이 될 것입니다!

이 가이드는 모델을 평가하는 다양한 방법, 자체 평가를 설계하는 가이드, 그리고 실제 경험에서 얻은 팁과 요령을 다룹니다.

프로덕션 모델을 다루는 전문가이든, 연구자이든, 취미로 하시는 분이든, 필요한 정보를 찾으실 수 있을 것입니다. 만약 원하는 내용이 없다면, 이슈를 열어주세요(개선 사항이나 누락된 리소스를 제안하기 위해). 가이드를 보완하겠습니다!

## 이 가이드 읽는 방법

-**초보자**:

  평가에 대해 아무것도 모른다면, 각 장의 `기본` 섹션부터 시작한 다음 더 깊이 들어가는 것이 좋습니다.

  또한 `일반 지식`에서 중요한 LLM 주제에 대한 설명도 찾을 수 있습니다: 예를 들어, 모델 추론이 어떻게 작동하는지, 토큰화가 무엇인지 등입니다.

-**고급 사용자**:

  더 실용적인 섹션은 `팁과 요령` 부분과 `문제 해결` 장입니다. `설계` 섹션에서도 흥미로운 내용을 찾을 수 있습니다.

본문에서 ⭐로 시작하는 링크는 제가 정말 좋아하고 읽기를 추천하는 링크입니다.

## 목차

이 주제에 대한 소개가 필요하시다면, 평가를 왜, 어떻게 하는지에 대한 이 [블로그](https://huggingface.co/blog/clefourrier/llm-evaluation)를 읽어보세요!

### 자동 벤치마크

- [기본](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/automated-benchmarks/basics.md)
- [자동 평가 설계하기](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/automated-benchmarks/designing-your-automatic-evaluation.md)
- [일부 평가 데이터셋](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/automated-benchmarks/some-evaluation-datasets.md)
- [팁과 요령](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/automated-benchmarks/tips-and-tricks.md)

### 인간 평가

- [기본](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/human-evaluation/basics.md)
- [인간 평가자 활용하기](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/human-evaluation/using-human-annotators.md)
- [팁과 요령](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/human-evaluation/tips-and-tricks.md)

### LLM-심사관

- [기본](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/model-as-a-judge/basics.md)
- [심사관-LLM 얻기](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/model-as-a-judge/getting-a-judge-llm.md)
- [평가 프롬프트 설계하기](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/model-as-a-judge/designing-your-evaluation-prompt.md)
- [평가자 평가하기](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/model-as-a-judge/evaluating-your-evaluator.md)
- [보상 모델은 어떨까](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/model-as-a-judge/what-about-reward-models.md)
- [팁과 요령](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/model-as-a-judge/tips-and-tricks.md)

### 문제 해결

이 가이드에서 가장 실용적인 부분입니다.

- [추론 문제 해결](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/troubleshooting/troubleshooting-inference.md)
- [재현성 문제 해결](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/troubleshooting/troubleshooting-reproducibility.md)

### 일반 지식

이것들은 주로 LLM 기초에 대한 초보자 가이드이지만, 여전히 몇 가지 팁과 멋진 참고 자료를 포함하고 있습니다!

고급 사용자라면 `더 나아가기` 섹션을 훑어보는 것을 추천합니다.

- [모델 추론 및 평가](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/general-knowledge/model-inference-and-evaluation.md)
- [토큰화](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/general-knowledge/tokenization.md)

### 예제

더 실습적인 평가 경험을 원하신다면 주피터 노트북 형태의 예제도 찾을 수 있습니다!

- [평가 중 작업 공식 비교하기](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/examples/comparing_task_formulations.ipynb): 이 노트북은 단일 작업에 대한 프롬프트 변형을 정의하고, 평가를 실행하고, 결과를 분석하는 방법을 안내합니다.

## 계획된 다음 글

- contents/automated-benchmarks/Metrics -> 자동 메트릭 설명
- contents/Introduction: 왜 평가가 필요한가?
- contents/Thinking about evaluation: 작업을 구축할 때 항상 고려해야 할 상위 수준의 사항은 무엇인가?
- contents/Troubleshooting/Troubleshooting ranking: 왜 모델 비교가 어려운가?

## 리소스

참조 링크

- [평가에 대하여](https://github.com/huggingface/evaluation-guidebook/blob/main/resources/About%20evaluation.md)
- [NLP에 대하여](https://github.com/huggingface/evaluation-guidebook/blob/main/resources/About%20NLP.md)

## 한국어 번역 관련

이 문서는 영어 원본의 한국어 번역본입니다. 번역 과정에서 다음 사항에 유의했습니다:

1. 기술 용어는 가능한 한 원래의 영어 용어를 유지하면서 한국어로 적절히 번역했습니다.
2. 번역은 원문의 의미를 최대한 보존하려고 노력했으나, 문화적 맥락이나 언어적 특성으로 인해 일부 표현이 원문과 다를 수 있습니다.
3. 링크는 원문의 영어 자료를 가리키고 있으며, 한국어 번역본이 별도로 존재하지 않을 수 있습니다.
4. 번역에 오류나 개선이 필요한 부분이 있다면 이슈를 통해 알려주시면 감사하겠습니다.
5. 이 번역은 커뮤니티의 기여로 이루어졌으며, 지속적으로 개선될 예정입니다.

최신 정보나 정확한 기술적 내용은 항상 영어 원문을 참고하시기 바랍니다.

## Citation
[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC-BY--NC--SA-4.0-lightgrey.svg

```
@misc{fourrier2024evaluation,
  author = {Clémentine Fourrier and The Hugging Face Community},
  title = {LLM Evaluation Guidebook},
  year = {2024},
  journal = {GitHub repository},
  url = {https://github.com/huggingface/evaluation-guidebook)
}
```

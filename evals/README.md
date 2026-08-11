# Saudi Legal AI — Evaluation Corpus

هذا المجلد يحتوي على corpus التقييم لمشروع Saudi Legal AI OpenClaw Edition.

## الهدف

قياس جودة الاسترجاع — **ليس** جودة التوليد. المقاييس:

| المقياس | التعريف |
|---|---|
| `citation_precision` | نسبة الاستشهادات المُعادة التي تطابق المصدر الصحيح |
| `source_recall` | نسبة المصادر الصحيحة المُسترجَعة من إجمالي المصادر المتوقعة |
| `abstention_accuracy` | نسبة الأسئلة الغامضة التي أُعيد فيها `insufficient_evidence` بشكل صحيح |
| `response_time_ms` | زمن استجابة الأداة بالميلي ثانية |

## معيار النجاح

> هل يسترجع المصدر السعودي الصحيح، ويستشهد به بدقة، ويمتنع بثقة عندما لا يملك دليلاً؟

## هيكل الـ corpus

```
evals/
  corpus/
    labor-law-questions.json
    pdpl-questions.json
    contract-risk-questions.json
  metrics/
    eval_runner.py
    results/
      baseline.json   ← ينشأ بعد أول تشغيل
```

## تشغيل التقييم

```bash
python evals/metrics/eval_runner.py > evals/metrics/results/baseline.json
```

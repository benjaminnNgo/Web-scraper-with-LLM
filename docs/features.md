# Available features

This documents provides high overview of features currently available in this code base

## Parse car description from VDP URL

To parse car description from VDP URL, you need to provide target URL at the endpoint at `/scraper` as follows:

```
http://127.0.0.1:8000/scraper/?url=replace_this_with_your_url
```

A `JSON` object containing description will be return. For example:

![img](img/case1.png)

### Study cases

1. Case 1

**Input:**

> https://www.bergeronchryslerjeep.com/new/Ram/2026-Ram-1500-for-sale-near-New-Orleans-a32be829ac182bc19058e5d1cb76bf57.htm

**Output**

![image](img/case1.png)

2. Case 2

**Input:**

> https://umanitoba.ca/

**Output**

![image](img/case2.png)

This is an interesting case where there are any car related information from the webpage. However, the `gemma3:1b` makes up responses (hallucinations issue).

However, if we use the same prompt template to ask `GPT-5` to perform the same task. The output will be empty string. May be `GPT-5` does a better job in preventing hallucinations compared to `gemma3:1b` (very tiny model that runs in reasonable time on CPU).

But still, can we prevent hallucinations of `gemma3:1b`? May be chain-of-thought helpful? Ask the model if the page contain any releated information about cars first? Then ask it to parse after that? This is actually very interesting to try and I am currently working on this improvement.

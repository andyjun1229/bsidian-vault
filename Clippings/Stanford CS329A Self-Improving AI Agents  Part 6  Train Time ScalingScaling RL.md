---
title: "Stanford CS329A Self-Improving AI Agents | Part 6 | Train Time Scaling/Scaling RL"
source: "https://www.youtube.com/watch?v=yVnmHSAy3ck&list=PLangBM27OtEA&index=6"
author:
  - "[[Stanford Online]]"
published: 2026-08-03
created: 2026-08-26
description: "Want to dive deeper? This curriculum is covered in the following online courses:- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html- XCS329 graduate course:"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=yVnmHSAy3ck)

Want to dive deeper? This curriculum is covered in the following online courses:  
\- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html  
\- XCS329 graduate course: https://online.stanford.edu/courses/cs329a-self-improving-ai-agents  
  
A similar curriculum is covered in XCS329z https://online.stanford.edu/courses/cs329z-engineering-ai-agents  
  
Follow along with the course schedule and syllabus: https://cs329a.stanford.edu/  
  
View the course playlist: https://www.youtube.com/playlist?list=PLangBM27OtEA  
  
Video Summary:  
This lecture video from Stanford's CS329A, Self-Improving AI Agents, taught by Aakanksha Chowdhery on October 10, 2025, covers train-time scaling and scaling reinforcement learning through three papers. STaR, the Self-Taught Reasoner, bootstraps reasoning chains through rationalization and filtering by answer correctness. DeepSeekMath introduces Group Relative Policy Optimization, a memory-efficient alternative to PPO, and shows gains from training on curated math data. DAPO addresses entropy collapse and training instability in reinforcement learning on long chain-of-thought reasoning through techniques including asymmetric clipping and dynamic sampling. Using the AIME math benchmark, the lecture traces how these methods let smaller models match the accuracy of much larger systems, and it closes with open questions on why majority-at-K accuracy improves while pass-at-K does not.  
  
Speaker Bio:  
Aakanksha Chowdhery  
Adjunct Professor of Computer Science, Stanford University  
  
Dr. Aakanksha Chowdhery is pushing the frontier of agentic LLMs, focusing on recursive self-improvement and long-horizon agents that learn and deploy in the real world. She is one of the few researchers globally who has led frontier model training end-to-end, across both dense and mixture-of-experts (MoE) architectures. At Google, she led the 540B PaLM model, the largest densely trained language model in the world at the time. She subsequently drove pre-training and scaling of Gemini's MoE models across multiple generations, and contributed key components to PaLM-E, Med-PaLM, and the Pathways infrastructure underpinning Google's large-model efforts. She went on to build and lead pretraining teams for open intelligence efforts at Reflection and Meta. Earlier, she held research roles at Microsoft Research and Princeton. At Stanford, where she earned her PhD, she teaches CS329A (Self-Improving AI Agents) and serves as Program Chair for MLSys 2026.

## Transcript

**0:05** · Welcome, everyone, to the sixth lecture for CS320A.

**0:09** · We'll today cover train time scaling or scaling RL.

**0:13** · So far, we have gone through several topics related to test time scaling, feedback using tools and code, and then also robust verification.

**0:24** · Today, we will see how we can close the loop to improve the models even further.

**0:30** · OK.

**0:30** · So today's lecture, we will actually cover three papers.

**0:34** · The first paper will cover how can you boost the reasoning capabilities of the models with putting rationales in problems.

**0:44** · This paper is called STaR.

**0:46** · It was actually done by an author at Stanford.

**0:50** · The second paper we will cover is DeepSeek math, which talks about mathematical reasoning and how that can be boosted in language models.

**0:58** · And then the third paper is more focused on reinforcement learning and how when you have to do reasoning with long reasoning chains, how can you stabilize that kind of reinforcement learning algorithms.

**1:11** · So to motivate a lot of the papers that we'll present today, if you look at a benchmark called AIME, so AIME is a benchmark, which is on mathematical problems, which tests for mathematical reasoning.

**1:30** · It's more complex mathematical reasoning problems than say, what was in a math benchmarks.

**1:36** · We used math benchmarks earlier this year, and then that one is already saturated and contaminated in most of the models.

**1:44** · Basically, most of the models have been trained on it.

**1:46** · So we had to change the benchmark.

**1:48** · So this is AIME 2024 and AIME 2025, the benchmark that you use in homework 1.

**1:54** · Is a recent benchmark that has mathematical reasoning problems.

**1:59** · And if you were to evaluate GPT-3.5, which is a 175 billion parameter model, you would get-- or that's what it's believed to be, you get almost 5% accuracy.

**2:10** · But if you were to take DeepSeekMath, which was using train time scaling on 7B model, it gets 51.7% accuracy, and with additional tricks, it's able to even get 60% accuracy.

**2:25** · And if you apply the third paper that I will talk about called DAPO on the Qwen-32B model, you are able to get 50% accuracy.

**2:35** · So in the prior work or in the first lecture, we were saying that as we scale the number of parameters in the model, that's when the model capabilities go up.

**2:47** · The model accuracy on benchmarks go up.

**2:50** · But what we are seeing in this particular slide is that you can achieve a pretty high performance on reasoning benchmarks with smaller models.

**2:57** · So how did these smaller models get really performant?

**3:00** · How did they get really high accuracy?

**3:02** · So that's something that we will explore in this particular lecture.

**3:07** · And some of the tricks that are being used to achieve this are called train time scaling.

**3:13** · So typically, if you try to do reinforcement learning on reasoning, it will not work well.

**3:18** · And a lot of the times, the reason it doesn't work well is because the implementation details are hard to get right.

**3:25** · So the key insights that we will study today are that if you have a model, earlier, you were just training it on internet.

**3:34** · So pre-training, the technique of model training, was training the model on internet.

**3:40** · If you allow the model to learn from their own outputs by filtering cleverly, you can improve the models even further, hence the class is called self-improving AI agents class.

**3:51** · And then the amount of compute you invest in training the model on its own outputs can substitute for the model parameters.

**3:59** · This also parallels some of the earlier efforts where the amount of compute used in training smaller models, if you could increase the amount of data, has been shown to help improve certain benchmarks.

**4:11** · And then the third point is that when you're doing reinforcement learning, as opposed to supervised learning, you have to really be careful about details of the implementation, because as you scale up those algorithms, the small fixes can be extremely important.

**4:25** · So the three paradigms that I'm talking about here are pre-training, which is basically training the model on internet that we have talked about in the first lecture.

**4:35** · And we're not covering that much in detail.

**4:38** · And then the next technique would be that fine-tuning, which is how you get your chatbots, where you're basically perhaps fine-tuning or doing reinforcement learning with human feedback or RLAIF on preference data from humans.

**4:51** · And then the test time scaling, which was some of the techniques that were covered in previous lectures.

**4:56** · Those are more techniques where you're basically doing some sort of say, majority voting or inference time sampling, and then combining the outputs from how you sample from the model.

**5:07** · For example, in homework 1, you are evaluating majority voting.

**5:11** · Then you are evaluating some other techniques that combine and evaluate the errors in what the model is producing and then using that to improve the model.

**5:21** · So test time scaling is mostly inference-based techniques.

**5:24** · Now, if you take what the model output filter after applying this test time scaling and then use that to fine-tune further, that's roughly what train time scaling is.

**5:34** · So if you take nothing away from this entire lecture, but you just remember this loop, then you have learned the basics of what train time scaling does.

**5:43** · Questions.

**5:47** · How do you know what is the good balance to distribute your compute into training time scaling versus test time scaling?

**5:54** · Is there a flat ROI curve that you reach at a certain point after investing in training time?

**6:01** · I mean-- Great question.

**6:04** · Let's hold that question until the third paper.

**6:08** · Cool.

**6:09** · But definitely ask that question again.

**6:13** · So roughly, what happened last year was that the reasoning model, this is a graph on o1 and o1's accuracy on AIME on the pass@1 accuracy on the y-axis, and then the amount of compute on x-axis and train time is shown on the x-axis, on the left graph, and test time compute is shown on the x-axis on the right-hand plot.

**6:37** · So what is happening here is that as we are increasing the test time compute that we have already seen, the pass@1 accuracy should go up.

**6:44** · So this is a log linear plot, and so more inference time compute better pass@1 accuracy.

**6:50** · But what they're also showing is that if you can increase the train time compute, then you can also improve pass@1 accuracy.

**6:57** · So what o1 showed for AIME benchmark was that by increasing both the train time compute and the test time compute, you are able to improve the accuracy on the benchmark.

**7:10** · So it allows you for basically a circular loop where you can generate model outputs and then feed them back to improve the model on this particular benchmark.

**7:19** · Now, why does this work?

**7:20** · So math is a domain in which there is verifiability.

**7:23** · So we had a whole lecture on robust verification.

**7:26** · So you have the ability to know which outputs are correct, and which ones are not correct.

**7:30** · So you have some ability to actually choose the correct outputs that can then feed into train time scaling.

**7:35** · So this works better in domains where there is verifiability.

**7:40** · So typically, why does reasoning start to help?

**7:44** · So this is a repeat of some of the slides, but I think it's very important to remind folks that all the reasoning models in all series are of Gemini flash thinking, or the equivalents in other frontier labs.

**7:57** · Basically, reasoning allows us to solve for difficult problems, because when you're solving a difficult problem, you will not just spit out the output, even in chain of thought and math problems.

**8:06** · When you were asking the model to think step by step, it allowed a certain amount of tokens to be dedicated to spelling out the reasoning and step by step process.

**8:15** · So thinking models use a chain of thought where when they're attempting to solve the problem, and what these tokens might get dedicated to is, you will see patterns like problem analysis, where they might actually try to understand what the problem is describing.

**8:28** · Task decomposition.

**8:30** · I'll show you an example of this where they try to decompose the task into sub-tasks.

**8:36** · Self-evaluation.

**8:37** · They might actually try to look at the answer, and then be like, OK.

**8:41** · This is not looking correct.

**8:43** · So they might actually choose to backtrack and recognize their own mistakes, and then backtrack to a previous step where they redo the problem.

**8:52** · And they might try some kind of different approaches.

**8:57** · So it's like a somewhat parallel search where they might actually try multiple approaches at the same time, instead of if the current one is not leading to a solution.

**9:05** · So it needs to have some sense of whether it's the correct solution or not.

**9:08** · So here are some examples from actually a earlier version of the model in o1 series.

**9:16** · So here, the user is requesting a batch script, where it wants to understand-- it's requesting a batch script that will represent a string with this format and print out the transpose in the same format.

**9:28** · So it's taking a matrix and printing the transpose.

**9:32** · And what you see in the output is that the model first tries to understand what the user is asking in terms of input and output formats before it tries to solve the problem.

**9:44** · So that's more of a problem analysis kind of pattern.

**9:47** · Another example for the same problem you see is that it tries to decompose the problem.

**9:52** · So it will actually-- once it understood the problem, it's saying that the approach should involve-- maybe I should parse the input string, then build a matrix, transpose the matrix, and then output the matrix in the same format.

**10:03** · So it's breaking it into multiple steps.

**10:06** · For this particular problem, this might be an overkill, but in more complex problems.

**10:10** · This might be a better way to solve the problem because you decompose the problem into smaller steps.

**10:15** · And then self-correction.

**10:17** · So this is a different problem from chemistry, where it's asking pH of some solution on a chemical and the model starts to compute the pH value, but then it suddenly has this notion of wait, the correct formula is different.

**10:33** · So it basically goes and changes the formula that it was going to use.

**10:37** · So even though it's pulling from the knowledge that the model already has, it's actually correcting itself.

**10:42** · So it has the capability of self-correction.

**10:45** · And how does this help the model?

**10:48** · So as I was trying to explain before, in domains where you have verification like computer programming or data analysis or mathematical calculation, the win rate over GPT-4o, which was not a thinking model, you'll see that it's greater than 50%.

**11:03** · So certain domains benefit way more from this train time scaling kind of techniques as opposed to if you look at personal writing or editing text, there's not as much improvement in terms of win rate.

**11:16** · Win rate means if you were to give humans output from GPT-4o versus thinking models, personal writing and editing text may not see as much gains, but domains which have the ability to verify and close the loop see more gains.

**11:30** · Questions?

**11:31** · Can you go back to help pages for us to compute \[INAUDIBLE\] So for that is a train pattern \[INAUDIBLE\] 0 times.

**11:48** · It seems that this time performance is better than the train pattern because all the writing seems \[INAUDIBLE\] on the right.

**11:57** · On the left that is not \[INAUDIBLE\].

**11:59** · So in this case, the \[INAUDIBLE\] performance increased better than the train performance.

**12:04** · So in this particular plot, it does look like that.

**12:08** · But that's kind of-- There is no intuition around these things as to like one should be better than the other, I mean.

**12:15** · This is one instantiation of where things were, and I just wanted to show you the curve.

**12:20** · It seems to me like test-time performance better than train-time performance-- Mhm.

**12:25** · That means something suspicious is going on.

**12:27** · Something suspicious is going on, OK?

**12:29** · I copied the plot.

**12:31** · So the graphs are not always right, as you might know from their latest release.

**12:35** · OK.

**12:37** · \[LAUGHTER\] OK.

**12:40** · So let's go back to the fundamentals, right?

**12:42** · So what is it that we're trying to answer?

**12:43** · I think the fundamental question we're trying to answer is that in test-time compute, you can basically if you go back to this plot, test-time compute is very cheap for someone to put, because you've trained a model, and then you can go and do multiple inferences.

**12:57** · And if one of the answers is correct and you have a good verifier on your end, then you can basically scale compute infinitely.

**13:04** · In fact, I think next Friday, I'll go through some papers, including \[? AlphaCode ?\] for example.

**13:10** · And what you will find there is that if you can basically make your search infinite in some ways, then in test-time you basically have a solution that will be correct, because from test-time scaling, we do know that there is a correct solution if you repeatedly sample, right?

**13:26** · Train-time scaling the challenge will be that you have to scale it correctly, which we'll cover in this lecture.

**13:32** · And then the second bit is that there's a certain amount of this closed feedback loop has to have enough successes for the train-time scaling to work well.

**13:41** · So you will see that in the papers that I will present now.

**13:45** · So that is actually different in the traditional machine learning to compare between the performance-- test that performance, because that \[? graph ?\] is showing it exactly more efficient if you cross the compute it to the \[? past, ?\] because one test-time compute increases the accuracy increase.

**14:02** · Like given the same compute to test, essentially, you have better performance.

**14:07** · So there is a caveat to what you're saying.

**14:10** · Test-time compute works well in benchmarks where the verifiability is robust.

**14:16** · OK.

**14:19** · Otherwise, you do need to get the model to start to reason better, and you need some verification loop.

**14:24** · So both serve there-- I mean, this is something we'll discuss in the lecture, but both serve their goals.

**14:30** · So if you prefetch what I'll present by the end of the lecture, when you look at a pre-trained model, what it is good at is it has a certain level of capability in, say, solving mathematical problems and solving reasoning problems and reasoning about finance or legal or whatever based on whatever domains it has seen already data in.

**14:50** · But then in inference time, you're basically getting it to reason over multiple of these traces and then picking one.

**14:56** · If you know and have a good way to verify the solutions, then you can pick one of the solutions.

**15:01** · That's like saying, I'm going to throw spaghetti at the wall, and I know where it should land.

**15:07** · Otherwise, with train-time scaling, you can teach the model and boost the path at 1 accuracy so that there's more likelihood that it will emit the correct output, but you still need verification of the loop.

**15:20** · More questions?

**15:24** · Yes So when you're fine tuning the model to be able to solve difficult problems better, does it have any regression on solving simpler problems?

**15:34** · And if so, how do you prevent that?

**15:37** · That one also needs doing.

**15:38** · Let's keep those questions.

**15:40** · I like all the questions, but we need to get to the first paper and then we can ask that one.

**15:48** · Typically, there shouldn't be a regression on solving easy problems if you're solving difficult problems, unless you're basically go into reasoning chains that are completely broken in some way.

**16:01** · So repetitive reasoning chains, which is called as overthinking.

**16:08** · So let's cover the first paper first, where we are basically teaching the model how to reason.

**16:14** · So we are boosting the reasoning capability of the model with reasoning chains.

**16:20** · So let's take a look at how we can do that.

**16:24** · So we already covered this earlier, and we showed this in the first lecture.

**16:30** · So chain-of-thought in large language models provides both interpretability, and if you ask the model to show its work step by step, then provides boost mathematical reasoning.

**16:40** · And we saw several benchmarks common sense reasoning and so on.

**16:43** · So we want to basically get the model to have strong step-by-step reasoning capabilities along solving any problem.

**16:52** · What is challenging with existing approaches, if you were to try to get this in existing approaches, so no internet scale data has really reasoning steps most of the time.

**17:00** · There are very few internet sources that have the large-scale reasoning steps.

**17:04** · And then if you try to manually annotate reasoning steps, that's very expensive because you literally need humans to annotate those reasoning steps.

**17:12** · And if you try to automate this process of generating reasoning based on known solution patterns, then that also works only in very, very specific domains.

**17:23** · And then if you try to few-shot prompt-- few-shot prompting means if you give it a few examples of here is a problem, here is a reasoning chain, here is an answer, then that still underperforms models that can be fine tuned on just larger data sets.

**17:38** · So basically, small amount of reasoning examples don't quite cut it, and you can just have a larger data set without reasoning chains.

**17:46** · So the key insight that STaR has is very simple.

**17:53** · This is a very simple example.

**17:54** · It will start with a small number of examples, that is reasoning steps.

**17:59** · It will generate solutions.

**18:01** · So say 10k problems.

**18:02** · 10k is a representative number.

**18:05** · And then it will only keep the ones that have correct answers, but it will generate these problems with rationale.

**18:11** · And it can fine tune on those, and it can repeat.

**18:13** · So it can repeat this loop.

**18:14** · So this what's new here compared to what we were doing in test time scaling is it's only keeping the ones that have correct answers.

**18:21** · Now, why did it not produce correct answers on the other ones, and what can we do with those particular set of examples?

**18:27** · So that's the other interesting bit.

**18:29** · So in certain problems where it could not solve the problem, the model got stuck.

**18:33** · So what we want to do is we basically, if we just fine tune on the correct examples, the model is not able to learn how to solve new problems.

**18:42** · Let me cover this slide, and then we can come back.

**18:45** · So there's basically no signal.

**18:47** · So what we do is we give the model the answer and ask it to explain backwards.

**18:51** · So it's almost like I have this question, I ask the model to produce the answer, but now the model did not produce the correct answer.

**18:58** · So I give the model the answer, and then I ask you to produce the rationale.

**19:01** · So, for example, the answer is 42 the human says.

**19:04** · And then the model generates the reasoning.

**19:06** · And then you can fine tune the model on, again, the problem rationale and the answer, but don't show it the hint as if it was solved directly.

**19:16** · So this helps you expand the training set to include more difficult problems now.

**19:20** · So basically, it allows you to bootstrap the reasoning capabilities and not just, say, limited to easy problems that the model could solve earlier, but now you can bootstrap it iteratively.

**19:32** · So you basically generate reasoning attempts.

**19:34** · You learn from successful reasoning paths where the quality of the reasoning paths is entirely based on things being correct.

**19:41** · And for failed attempts, you're basically rationalizing them by saying, OK, here is a hint.

**19:47** · Please generate the rationale.

**19:48** · And then you're using these generated rationales as the training data.

**19:52** · So that's basically the algorithm that they use in STaR.

**19:55** · It's very bare bones, and like you can almost call it an off-policy reinforcement learning technique.

**20:00** · It's a very bare bones way of producing reasoning techniques in a model.

**20:07** · And the assumption that is being made in this particular case is that how do you know something is a good rationale?

**20:13** · They're assuming that if the model output is correct, which in math they found that was generally true, the correctness of the final output is a proxy for the reasoning quality.

**20:23** · So they're filtering incorrect answers.

**20:25** · Basically, they're assuming that will be filtering out lower quality reasoning chains, but there might be scenarios where they're not learning from incorrect reasoning chains as a result.

**20:37** · But they get higher quality training data.

**20:39** · And then the second bit is that they assume that the language model can generate valid reasoning paths when it's given the answer as a hint.

**20:47** · So it assumes that if I show the model the answer and then ask it to show its work, it will be able to do so.

**20:53** · And then finally, there is some amount of assumption that the initial language model is strong enough to bootstrap from few short examples.

**21:02** · So if the class of problems is way outside the capability of the initial language model, then it will not make much progress on this.

**21:09** · And this is where the iterative aspect starts to become important.

**21:13** · I was seeing a couple of hands, so let's take them one by one.

**21:17** · Yeah, I was just wondering, so do they start with a math data set that has the correct answer?

**21:24** · It just doesn't have reasoning, right?

**21:25** · Like that's how they know what the correct answer is.

**21:27** · Yes.

**21:28** · OK.

**21:29** · Because I was like, how do they know the correct answer?

**21:31** · Yeah, everyone is starting with a benchmark basically.

**21:35** · Yes.

**21:35** · Is there filtering that happens for step three?

**21:39** · Like, are we worried that we give the correct solution, and then there's issues in the reasoning just to get to that solution?

**21:46** · So they actually don't filter in step three, but there are follow-on papers that do filter in step three.

**21:52** · I mean, you can do some sort of process-reward model on top of the reasoning chains, and then say which of the steps makes sense or which of the steps don't make sense.

**21:59** · But this particular paper was one of the first.

**22:01** · I mean, one of the attempts in this class is to show you papers as they evolved as opposed to what's the latest paper here.

**22:10** · But yes, you can-- that might be another project idea of how do you evaluate the quality of the reasoning chains if you don't want to depend on just the final outcome as the proxy for correctness.

**22:23** · Yes.

**22:24** · So the problem is too \[INAUDIBLE\] it fails as a pattern.

**22:29** · Even if you tell the model the right answer, it's tests do not do well, because it's just too complicated to look at the model.

**22:39** · That's a great question.

**22:40** · So, as I told you in step four, the assumption is being made that the benchmark on which this is being done is essentially where the problem is not too difficult.

**22:53** · It is within range, or some subset of the problems are within range of the language model.

**23:00** · And typically you can-- so that is an assumption that is made.

**23:06** · And then when you do iteratively, the model might get better at certain point that it can start handling these other problems.

**23:13** · I have a question in step three.

**23:15** · So in the NLP like \[INAUDIBLE\] direction.

**23:24** · So I'm just wondering, is there a possibility that you can know from the step two \[INAUDIBLE\].

**23:30** · And in step three \[INAUDIBLE\] you just use \[INAUDIBLE\] So that's a great point.

**23:43** · Let's come back to that one.

**23:44** · So I think what I'll show you by the end of the lecture is that learning from negative examples has not been nailed.

**23:50** · Learning from positive examples has been.

**23:52** · Like, if you have any non-zero reward, then you have an ability to close the reinforcement learning loop, which is not happening yet in this particular set of examples.

**24:02** · So you do need to be able to close the loop in some way.

**24:07** · So if you have negative examples, there are some papers that have tried to learn from it, but that's not something we'll cover today.

**24:16** · Yes.

**24:17** · I have a similar question worrying how to evaluate or verify the quality of the generated rationales on this failed attempts after giving the hints, like since the model already know the answer, but it might generate incorrect reasoning that leads to \[INAUDIBLE\].

**24:37** · So that's a great problem too.

**24:39** · So you're saying that in step three it might generate wrong rationales is what you're saying?

**24:46** · Yeah.

**24:47** · Then it will learn wrong reasoning from correct attempts.

**24:51** · Yes, that will be a problem.

**24:53** · In this particular case, they don't have any further filtering on top of rationales.

**25:00** · So there would be no way to hill climb in that case.

**25:04** · You can have humans look at the reasoning chains.

**25:08** · It could be tedious, yes.

**25:13** · OK.

**25:13** · So going through this in a little bit more rigorous detail.

**25:17** · So you start with a prompt data set where you have the questions, the rationales, and the answers.

**25:22** · This prompt data set will be small, and compare it to the amount of data that we want to train on.

**25:29** · For example, this is the multiple choice questions.

**25:32** · Where do you put your grapes just before checking out?

**25:34** · There's a rationale, and then the correct answer is for example B, which is grocery cart.

**25:39** · Now, you have a training data set which is quite large of examples that have questions and answers.

**25:45** · This would be, say, if you have a benchmark, you might have a trained subset of the benchmark and a test subset of the benchmark.

**25:52** · And what Vanilla STaR will do is it will start with this rationale data set and training data set.

**25:57** · So it will first few-shot prompt the model with the rationales in the Rationale data set.

**26:02** · And then it will get the model to produce the rationales and the correct output.

**26:09** · So this is on the training data set.

**26:10** · So now it's few-shot prompting, but it's supplying questions from the training data set, and it's checking if the answers are correct by the language model.

**26:20** · And it will collect these set of rationales that it can use, and then it can fine tune the language model on these correct solutions.

**26:29** · If you have a rationalization, which is what STaR does, if the answer is incorrect, what you will do is you will add hint.

**26:37** · So you'll be saying, OK, here is the correct answer, and you will essentially generate the rationale by looking at this hint, and then you will use that to add to that data set of rationales that led to the correct answer.

**26:50** · And then you can fine tune on top of that language model.

**26:53** · And so you basically have these two sets of rationales that then you can fine tune on top of this language model, and you can do this process iteratively.

**27:01** · So you don't do it just once.

**27:03** · You fine tune it.

**27:04** · Now the language model perhaps is able to produce better reasoning chains.

**27:08** · So now you can, again, start with your training data set, and whatever was not correct, you can redo this process.

**27:14** · So their experiments were on a small model, which is an open source of GPT-3, a 6 billion parameter model called GPT-J. They had a pretty small warm-up, and then they kept a constant learning rate, and then they basically had certain number of iterations of the outer loop.

**27:30** · And then they increased the number of steps in the inner loop on each step.

**27:35** · So one of the comments the paper makes is that they want to have a slower start in the training time, and then they want to slowly increase the number of things that are happening in the inner loop.

**27:49** · The data sets that they tried this on was GSM8K.

**27:53** · So GSM8K is just math problems that you have seen where you're basically asking-- this is a grade school math problems.

**27:59** · There are about 9k samples.

**28:01** · Then CommonsenseQA.

**28:02** · CommonsenseQA is essentially problems that you would see on, say, related to day-to-day stuff.

**28:09** · So you will have these multiple-choice questions, and then you have these answers, and there's rationalization that looks like this.

**28:15** · And then arithmetic problems, which basically was some sort of an addition problem on multi-digit addition.

**28:22** · So they generate the last one was synthetic data where like they generated some of these things themselves.

**28:30** · So in terms of results, some of the results that stood out in this paper was that just compared to, say, supervised fine tuning on, say, math benchmark, they could boost with this STaR approach to 51.7%, but they only use 70% to 87% of the data in terms of-- so they had to throw out a whole bunch of data that did not have correct solutions.

**28:52** · And other challenge is that it's not really true RL.

**28:56** · So if you basically do multiple iterations of this, it starts to plateau after a while.

**29:01** · So, I mean, RL has its own set of challenges, but here it also starts to plateau.

**29:07** · So you have to really pay attention to how many iterations you can do.

**29:11** · And there's some amount of tweaking there that you have to do.

**29:16** · The other interesting set of results here were that this was on a common sense reasoning.

**29:22** · So they actually looked at-- this was a question that several folks asked here.

**29:27** · They actually tried to see the rationales for CommonsenseQA.

**29:30** · They showed it to human raters, and they asked human raters to say how likely they are to prefer the rationales from STaR versus just like otherwise.

**29:43** · So STaR generated rationales versus the few-shot rationales in the Rationale data set.

**29:49** · They compared those.

**29:50** · And what they found was that generally, the qualitative analysis showed that their rationales were pretty reasonable.

**29:58** · Now, CommonsenseQA, as you remember, is a natural language like it's tackling daily problems here.

**30:04** · So as a result of that, the rationale seemed pretty reasonable.

**30:09** · And then the other aspect that they noticed was that STaR, in general, requires-- like, if you use direct fine tuning, you basically do get a certain level of accuracy.

**30:19** · But STaR with rationalization gets that accuracy, but it requires much less data compared to what you would need for fine tuning.

**30:28** · So rationalization helps you get to an accuracy using like-- so 86% of the data is used, but you can basically get to the deficit accuracy of 72.5% compared to using a lot of training data.

**30:43** · So this was a very small model.

**30:44** · So this was the first signs of life that was shown for reasoning.

**30:48** · In terms of mathematical reasoning, this was an interesting one on GSM8K.

**30:53** · What they found was that the use of rationalization actually did not improve performance.

**30:57** · So like STaR by itself was not helping in this particular case.

**31:01** · So what you see is that you have GPT-J like, basically, it improves over the baselines, but it's basically not helping too much.

**31:10** · If you directly do fine tuning on good data, then you can actually improve it similarly.

**31:17** · So one of the reasons that is the case is the number of calculation steps that were used by the model themselves.

**31:23** · If you force the model to use chain-of-thought versus you provide these rationalization steps is actually pretty similar.

**31:29** · So in some ways, it was not helping.

**31:32** · If the problem is too simple.

**31:34** · Like, the whole notion of getting the model to reason if the problem is too simple was basically not helping.

**31:40** · So GSM8K for GPT-4o was very much within capability.

**31:44** · So similarly for GPT-J, so there was not much improvement here relative too.

**31:50** · But it did show that direct fine tuned versus STaR with rationalization you still had some gains.

**31:56** · So some takeaways here are that the whole notion of rationalization conditions on the fact that you have an answer, and then you can essentially figure out what rationales would be good.

**32:09** · And the outputs without rationalization are examples where the model is already quite confident.

**32:15** · But then if you can look at the answer, then in certain cases, it might actually do a better job producing the rationale.

**32:24** · And if you do few-shot prompting, you can basically really help the model in how it should produce rationale.

**32:31** · But the style of rationale might actually influence the model in certain ways.

**32:38** · Like prompt engineering, in this particular case, might bias the model in certain ways.

**32:43** · So effectively there are certain challenges.

**32:46** · One challenge is that the rationalization the quality has certain amount of effects.

**32:51** · And the second bit is that if your few shot prompting, then you are biased by how the rationales were formatted in your few shot prompts, and that might affect what kind of rationales the model would produce and what you're training on.

**33:06** · So, overall, I think, this kind of gives us a sense of just that in the model space, if you basically bootstrap the model to generate rationales, you can get high sample efficiency while not having to get humans to generate these reasoning chains.

**33:21** · And you can apply it to many problems.

**33:23** · Like you can apply it to symbolic problems, natural language, mathematical reasoning.

**33:27** · Some of the challenges that are there in this overall techniques is that you don't have a very good evaluation for rationales for most tasks, because you basically have to have a human evaluate them, or you need some sort of a process-reward model to evaluate them.

**33:42** · There might be true negatives and false positives.

**33:46** · So you're just filtering based on correct answers, so you might have some invalid steps in between which might cause problems.

**33:52** · Yes.

**33:54** · So this method is useful for frontier models, right?

**34:01** · Because if you want to find a small language model, you can just use a faulty model to generate these training data.

**34:10** · I don't know how to answer that question.

**34:14** · You're saying that-- You don't have to rely on a small model to generate this new additional data automatically.

**34:22** · I see.

**34:23** · You can just use a big model, and it can train new stuff.

**34:26** · But I'm wondering the main benefit.

**34:29** · I mean, you are actually getting training out from nothing.

**34:34** · What it shows when you are training something, which is basically the form.

**34:40** · Yes.

**34:41** · So the goal for a lot of the work that we're discussing is the ability to-- I mean, we're showing the solutions on small models, but at the end of the day, what we want to be able to do is take the model, take its outputs, and then use that to improve the model.

**34:59** · You can always take a more powerful model and use it outputs.

**35:01** · And that's like distillation process.

**35:05** · Yeah, that's great, I mean, the theory.

**35:08** · Yes.

**35:09** · It's clear, but when it comes to practical applications-- Yes.

**35:13** · So I will use this method \[INAUDIBLE\] to pick the next, I don't know, 1 trillion parameter model, and I need additional data, \[INAUDIBLE\] more data.

**35:29** · But that's a fair point.

**35:32** · Or you want to basically improve the model on certain set of capabilities that they actually don't have.

**35:38** · They won't produce good model outcomes on.

**35:41** · So what I mean is that so if I want to improve the performance of a 7 billion parameter model-- Yes, in practice.

**35:51** · --then I wouldn't use this, because I get high quality data from distillation.

**35:58** · \[INAUDIBLE\] is much higher.

**35:59** · Yes.

**36:00** · We are not covering distillation, but that's fair point.

**36:03** · OK, thank you.

**36:03** · Just wanted to clarify.

**36:04** · Oh, no, that's a fair point that you can use one of the frontier models and distill things.

**36:08** · But this is more an attempt to build it from scratch and for you folks to understand what might that take.

**36:16** · Yes.

**36:17** · I have a question.

**36:19** · I'm curious about why this isn't like full-fledged RL, and also whether-- You're leading me to my next slide.

**36:26** · OK, great.

**36:27** · Oh, and also, I'm also curious.

**36:31** · So when you would decide to make the choice of to first train with SFT versus RL, if there's any different implications of how much data or compute is needed?

**36:43** · Hold that question until the end.

**36:45** · \[LAUGHS\] But I'm covering that.

**36:47** · That's part of the lecture.

**36:53** · So in STaR, you basically were just using the correct output, which is like a proxy for a verifier where you already know the answer.

**37:01** · If you basically also add a verifier in that whole loop, then that would be called V-STaR.

**37:07** · So there was a paper that basically had a generator and a verifier training in a loop.

**37:11** · And then Quiet-STaR was essentially adding an internal thinking.

**37:15** · So what it was doing was essentially instead of having reasoning steps be in the language space, it was actually putting reasoning steps in the latent space with MLPs.

**37:27** · So why have them in English when you can have them have the model thinking internally?

**37:34** · So before I move further, actually there have been a lot of questions.

**37:37** · So I'll only pick one of these questions.

**37:39** · But let's look at question 2.

**37:43** · What bounds the performance of STaR as an approach?

**37:53** · You can talk to someone for a minute, and then let's chat as a class.

**38:02** · Let's come on back as a class.

**38:04** · So what performance-- like how's the performance of STaR as a technique?

**38:08** · Any takers for that?

**38:19** · I'm seeing no hands.

**38:20** · You guys are talking.

**38:21** · All answers are welcome.

**38:27** · Yes.

**38:27** · I think this is kind of like a silly answer.

**38:29** · We were thinking, like, there are some logical steps that are more complex than others, and you wouldn't expect STaR to be able to make any logical leaps that are not in its training data set.

**38:40** · Like the rationalization should all be at the same level as what it was trained on.

**38:47** · This allows it to get more rationalization data.

**38:53** · OK.

**38:53** · So it will not make-- I mean, it will basically not have a logical leap into new domains that will have figured out new things is what you're saying.

**39:01** · OK.

**39:04** · Any other takers?

**39:06** · Yeah.

**39:07** · \[INAUDIBLE\] like absolutely \[INAUDIBLE\] because if the model is really bad at creating new logistic reasoning to introduce raw samples into the training \[INAUDIBLE\] Say that loudly what you're saying.

**39:33** · Yeah, so it seems like this performance is \[INAUDIBLE\] bounded by model's capability to do reasoning because-- I see.

**39:42** · Yeah.

**39:43** · If the model can't reason when given the hints, that's also not going to work out because the rationalization won't show up at all.

**39:50** · Yeah, and raw samples into the data.

**39:54** · That opens the question what needs to rethink in the base model?

**40:01** · I think some answers make it inherently easier to rationalize than others.

**40:06** · For example, if the final answer is like 225, you probably know that at some point, there's a multiplication of 15 and 15 or something similar to that, but maybe some other numbers are not as straightforward.

**40:16** · And I also think that if there's a lot of problems that you don't know the answer to and that forces you to rationalize, then you probably need more data so that you can form more generalized reasoning to backtrack.

**40:28** · OK.

**40:29** · I mean, that is in the right direction.

**40:31** · Yes.

**40:35** · OK.

**40:36** · I think all of these answers are fairly valid, but I think this is worth keeping in the back of your mind as you move into RL, because a lot of the magic in this particular domain is like, what can the base model do as we're building on top of that?

**40:51** · So we'll come back to that.

**40:53** · So the second paper that we'll cover is DeepSeekMath that will focus on mathematical reasoning.

**41:00** · And it will actually use a form of RL that it proposed that has become quite popular.

**41:05** · So we already looked at this graph earlier where we were basically showing that in math domain, if you do train-time scaling, you can do much better.

**41:12** · And OK.

**41:15** · So what this slide is showing is that if you look at the performance.

**41:19** · So this is a earlier benchmark than AIME.

**41:21** · It's actually a simpler benchmark than AIME.

**41:23** · It's called Math benchmark, and you're basically looking at Top 1 accuracy.

**41:27** · So if you look at the date of the benchmark, you'll see that as the model size is increased, typically, the accuracy on this benchmark has gone up.

**41:35** · But then suddenly when DeepSeekMath came out, 7B model was doing really well.

**41:39** · And the main leap that they made was that they were able to do the reinforcement learning part in the train-time scaling loop correctly.

**41:47** · So we will see what led to that innovation.

**41:51** · So the first thing that they got right was that typically when you try to improve on Math, and this was something that was done on top of PaLM as a paper, PaLM model.

**42:00** · There was this paper called which improved PaLM model on STEM.

**42:05** · And what they did was they trained on a lot of science and math data, typically like archive data.

**42:11** · What DeepSeek did it was like, OK, actually, training on archive papers is not the trick.

**42:16** · They actually trained on Common Crawl web pages, but they started with a DeepSeek coder model.

**42:22** · So they said that if you start with a model that has already been improved on code reasoning, then it will actually do better.

**42:29** · And then they did a really good job at curating from content from Common Crawl pages on math.

**42:37** · And they found that often arXiv papers in some ways don't have an adequate amount of math content that give us coverage.

**42:45** · So OpenWebMath by curating that and mining it and getting better coverage across math domains, they were actually able to get much larger yield in number of tokens.

**42:58** · And that was their first exercise in priming the model before they take it to RL.

**43:04** · So this was related to one of the comments that were made that if the model is not strong in a certain domain, you do have to improve its capability in that domain.

**43:12** · So this is that step.

**43:14** · So they basically got coverage across a lot of math domains, showed it a lot of high quality data in math, and they started from a code pre-trained model.

**43:23** · And so they actually showed that archive training was actually not really helping, but code to math significantly helped because it allowed the model to reason better, to tool use better.

**43:34** · This was actually the first time that this was shown that if you start from a coding-based model, you could do better.

**43:41** · And then the other thing that they showed was that the curation of data really helped in this particular case.

**43:48** · Now, the second step that they did was, OK, now that you have trained the model on math using supervised fine tuning, what do you do next?

**43:59** · So they actually scale up their RL.

**44:01** · Now, the typical RL algorithm that has been used in RL for human feedback, even with verifiers is called PPO.

**44:08** · So you have to keep your policy and your new policy.

**44:11** · So you basically this ends up being a memory problem if you try to do it on larger models.

**44:15** · Like 7B model is fine, but if you try to scale up RL, you have to keep multiple policy models, and then you also have to learn a critic model and a reward model.

**44:24** · So typically, in the RL loop, you have an old policy, a new policy that you're learning.

**44:29** · You have a critic that's basically giving feedback.

**44:32** · And then you have a reward model that's assigning the rewards.

**44:35** · So keeping all four of the copies of models starts to become challenging.

**44:38** · So what they did was they proposed a new technique called GRPO, where instead of having a critic or a value function estimate things, they basically use some sort of a generalized advantage estimation that I'll show you in the next slide.

**44:53** · And then you only have three copies of the model.

**44:55** · So now the PPO, which needed a lot more memory, instead of that GRPO essentially could use just a group for the baseline.

**45:04** · And the way that works is that for each question, you sample a lot of the answers.

**45:10** · And then you score them, and you normalize the reward of-- so this is the score that you gave for each of the answers using the reward model.

**45:18** · And then you normalize the reward as reward minus mean of rewards divided by standard deviation.

**45:22** · And then this becomes your advantage basically.

**45:25** · So typically, if you look at the way DPO works or all of those techniques works, you're basically going to compare the rewards.

**45:33** · So by doing a reward minus mean of rewards divided by standard deviation, you're effectively providing a comparative technique across rewards.

**45:42** · And the why.

**45:45** · So the reason this made sense was because reward models are going to essentially be trained on comparisons anyway.

**45:50** · So by providing the group context you can save memory, and now you can start scaling up RL.

**45:55** · And your advantage function in this particular case is essentially-- so I didn't add the full formula because I just wanted you guys to have intuition.

**46:02** · You could just take the reward, subtract the average reward, and then divide that by the spread of rewards.

**46:07** · And you can get an estimate of the advantage.

**46:09** · And on Math, they were able to go from 46.8% to 51.7%.

**46:14** · And this was actually the first open source model at 7B scale that crossed like 50% without having a critic.

**46:20** · This is a much earlier paper, but then this gives you a sense of the technique that they used.

**46:25** · And further, what they showed was that if you look at different variants of RL, effectively what you're changing is either the data source.

**46:33** · So I showed you how they curated their data.

**46:35** · And then you're deciding how to compute the gradients.

**46:39** · The gradient depends on gradient coefficient and the probability of the output given the question.

**46:45** · So the gradient coefficient computation changes in different algorithms.

**46:48** · So their estimate of gradient coefficient was coming from this group estimator group baseline, which worked well for a single-step problem where you're just trying to get the answer.

**47:00** · So if you compare approaches like STaR, where you basically are just generating things once, and if you get correct one, you basically get a reward of 1 if it's correct and 0 if it's wrong, or if you do online rejection fine tuning, you are still generating things online, but you only get a reward of 1 if it's correct and 0 if it's wrong.

**47:22** · So you basically reject anything that is incorrect.

**47:25** · GRPO is generating rewards online with a reward model, but it's basically getting an advantage function because you're doing multiple samples, and then you're giving them a score.

**47:35** · And the advantage for that score comes from this group baseline by computing the mean and then dividing it by the spread of rewards.

**47:43** · So now you can ask me the question that you were asking me earlier about the difficulty of the problems.

**47:50** · Oh, the difficulty of the problem that I make regression on simpler questions.

**47:56** · Yes.

**47:57** · Yeah.

**47:57** · So I'm curious if you are updating the model with fine tuning for difficult questions, you are essentially updating all the weights.

**48:09** · So isn't that going to potentially, theoretically, have any regression on simpler questions or other metrics?

**48:15** · So this is the table I wanted to show you.

**48:18** · So effectively, if you're basically trying to close the loop, what you're trying to figure out is how much reward you're giving.

**48:25** · So simple problems effectively, might equate you're going to get a reward of 1 anyways, and you're never getting a reward of 0.

**48:33** · And with GRPO, you're getting some form of a distribution of rewards that I was showing here.

**48:39** · So if you don't have any distribution and rewards, then-- so effectively what you want is some form of a distribution of rewards across the set of problems you are showing.

**48:49** · If there is not a distribution of rewards, there is nothing for the model to learn.

**48:52** · Like, if all the rewards are 0 or all the rewards are 1, then basically the normalization doesn't work.

**48:58** · Does that make sense?

**49:01** · Yes, but-- This we will solve in the next-- the shortcoming of this particular method we will solve in the next paper.

**49:09** · But this reward is specific to like this one particular feature that we're trying to train and not the basic overall holistic benchmark that we trained for the previous model before.

**49:23** · So I mean, it's basically taking problems and then computing answers, right?

**49:29** · If across the model, you basically are showing problems that are all very hard, then the model has no capacity to learn because it will basically have no reward at any point.

**49:39** · I see.

**49:41** · It needs some hill climbing signal, right?

**49:43** · Again, I'm not showing you a formula.

**49:46** · I'm intuitively explaining it to you.

**49:49** · Yes.

**49:50** · Oh, yeah.

**49:51** · Actually, I just wanted to comment on that piece quickly.

**49:54** · I think my interpretation of actually the solution to that is in the original paper is like, oh, PPO that's why there's a KL divergence term.

**50:02** · OK.

**50:02** · So essentially, it is a valid concern, because it's like we're updating the weights.

**50:06** · We could probably \[INAUDIBLE\] far like-- Oh, I see.

**50:08** · --the model.

**50:09** · And maybe we can get really good at answering these benchmarks.

**50:11** · But if we got really optimized on all these several benchmarks earlier \[INAUDIBLE\].

**50:16** · Also, I think, in addition to the normalized rewards, we also have somewhat divergence of penalty and policy conditions.

**50:23** · OK, that's a fair interpretation that you add KL divergence, and then you don't deviate from what it could already solve.

**50:31** · OK.

**50:32** · Yeah, I was interpreting it more along the lines of how do you have good distribution of problems so that the model has the right hill climbing signal, but I think what you're saying is that if the model could already solve something, then KL divergence solves that part of the problem.

**50:46** · OK.

**50:46** · Thank you.

**50:47** · I was listening to the question is like, so if you are trying to post train so that it has a new feature, do you really have to update all the weights?

**50:57** · No, I don't think so.

**50:58** · I mean, there have been some more recent works that have shown-- there are some blog posts that have been recently shown that you can do with lower updates and so on.

**51:09** · So I do think that KL divergence or some subset of features could solve that problem.

**51:15** · I think the reason this is interesting is that you want perhaps that these kind of techniques allow you to improve the model overall.

**51:27** · Yeah.

**51:30** · More questions?

**51:32** · We have a mindset of just have more compute be like, I don't know, like whether it's 0 or 1.

**51:37** · But for this one, how do you come up with a key-node score?

**51:42** · How do you come up with a clean score?

**51:44** · A key-node score.

**51:45** · Oh, because you train a reward model, right?

**51:49** · I mean, you can also have zeros and ones there, and then you can average things but-- So zero or one is like, say, how do \[INAUDIBLE\]?

**51:59** · So what I was showing you is you are training a reward model that is basically going to give you a score for that feedback.

**52:06** · Yeah.

**52:07** · If you only use 0 and 1, that can be a proxy, but then you can do some averaging.

**52:17** · OK?

**52:19** · So what this roughly tells you is that if you do basically the online reinforcement learning loop and you sample from the current model, that beats what we were doing earlier, we were in STaR approach.

**52:31** · So overall, what they showed was that you can improve the majority of the-- like, if they had 32 tries, it was improving the majority at K, but it was actually not improving past K.

**52:42** · So if you were basically looking plotting past K, say, one is correct.

**52:48** · If you sample 32 times, then that was not what was improving in their paper.

**52:52** · What was improving was that majority of the solutions become correct.

**52:56** · That's what was improving in this particular paper.

**52:58** · So the model actually became more consistent, not fundamentally smarter, was what they showed.

**53:06** · Now we'll cover the last paper called DAPO, which is basically going to fix some of the problems with respect to reasoning on harder problems.

**53:16** · So if you naively scale up GRPO and want to do this on even a Qwen-32B, model, which is very easily accessible, you would get 30% on AIME benchmark.

**53:27** · And here I will show you a lot of technical terms, but I will try to explain to you intuitively some of the challenges in just doing this on Qwen-32B ends up being like the entropy of the model collapses.

**53:39** · The model can become too confident.

**53:40** · The training can become unstable.

**53:42** · And the response length, the model output length, can become uncontrollable.

**53:47** · Like it can explore uncontrollably.

**53:48** · But DeepSeek did get 47% on AIME.

**53:51** · Like the DeepSeek carbon paper did get 47%.

**53:54** · So "DAPO," as a published piece of work tries to make explicit what were the techniques in RL that were not covered in, say, GRPO.

**54:05** · So some of the techniques that they talk about is that in PPO you have to do-- so you're basically trying to do some sort of exploration in your standard PPO algorithm.

**54:15** · And the standard PPO clipping treats the increasing and the decreasing on that very similar.

**54:24** · So basically, if you have a low probability token, it can only hill climb so much, and then the high probability token can also get clipped.

**54:32** · So the exploration can collapse.

**54:34** · So basically, the clipping function in the PPO algorithm needs to be asymmetric, and that will allow bigger increases.

**54:41** · So that was the first thing that "DAPO" found.

**54:45** · In terms of graphs, what that really meant was that if you did clipping, then your accuracy was much better.

**54:52** · And if you could allow clipping higher, if you could allow asymmetric clipping, the purple plot shows you that you could achieve much higher accuracy, and your entropy on the right side stayed more stable and did not collapse.

**55:04** · While if you did have-- did I invert that?

**55:08** · So this is higher accuracy, and then the entropy is looking nicer.

**55:11** · And then if you did not do asymmetric clipping, then your entropy has collapsed.

**55:16** · So entropy is a proxy for how much exploration is possible in the model.

**55:21** · A second very interesting technique, which actually relates to what we were talking about earlier, was something called dynamic sampling.

**55:30** · So what I showed you for GRPO was that, OK, you go and sample 64 solutions, and then you come up with a distribution on them, and then you take a group baseline.

**55:40** · What DAPO said was, OK, well, how about we oversample?

**55:44** · How about we don't just use 64 samples?

**55:47** · How about we oversample?

**55:48** · And then what we want is that we will filter out things that have zero reward and one reward so that what we want is basically a nice distribution so that most of the solutions have some sort of a signal.

**56:01** · So they filter out all correct and all wrong groups, and they keep only some subset between 0 and 64.

**56:09** · So they're basically doing dynamic sampling because they don't want to waste their gradient.

**56:14** · Your advantage should not be 0.

**56:16** · Like, if basically your rewards are all correct or all wrong, then those groups are filtered out, and you essentially want to keep only those groups that have some signal.

**56:27** · So this maintains an effective batch size because in RL, if you have effective batch size for propagating the gradients because you're not computing gradients from all correct and all wrong anyways.

**56:38** · Questions?

**56:43** · That's cool.

**56:44** · Did you find a conclusion \[INAUDIBLE\] Great question.

**56:47** · Yes.

**56:48** · So you have a batch of questions when you are training and then you're filtering out questions.

**56:56** · Yeah.

**56:58** · It seems 64 samples is quite small.

**57:01** · I'm wondering if it's because there's very limited amount of AIME questions out there and whether that was enough?

**57:10** · So this is a more an exemplar here.

**57:13** · You can choose how many samples you pick, but at the end of the day, this is mostly to showcase what was possible from their paper.

**57:22** · So AIME yeah, this would be benchmark specific and the difficulty of the benchmark and the capability of the base model.

**57:32** · I think the third bit that is worth noting is that the reasoning chains have a certain amount of length that matters.

**57:40** · So if you are basically doing a sample level loss or sample level means that for each question and answer pair, that that sequence you're computing a loss, then each answer is basically counted globally.

**57:51** · So in certain cases, if you have a very long garbage answer in the model output, then that basically gets same weight as a short good answer.

**58:01** · So they effectively suggest that you should have some effectively length penalty, which should put a better-- they want to shape based on the length, so they put a token-based loss as opposed to putting a sample-level loss, and that they gave them some gain.

**58:17** · And in particular, what they were controlling for is both the entropy and the mean response length.

**58:22** · So effectively, if they didn't have a token-level loss, they were noticing that the entropy was growing, and the response length was also not looking like it was growing uncontrollably.

**58:32** · So they wanted to shape that better by putting some form of a penalty there.

**58:38** · So they put a token level loss for that.

**58:41** · And then finally, there are certain cases in which the model encounters a hard problem.

**58:50** · So it basically gets truncated at the end, because it was thinking, and it was basically producing model outputs.

**58:57** · And these truncated reasoning chains can generate a lot of noise.

**59:01** · So they basically put a gradual penalty in the tokens to deal with that, and that allowed the training to become stable instead of adding noise.

**59:10** · So effectively, the generation entropy instead of becoming unstable once the model was learning to generate like really-- the model as it progresses starts to generate longer and longer reasoning chains and that can get truncated and that can cause problems.

**59:27** · So there are a couple of different ways in which different papers have tried to tackle this.

**59:31** · One is that either they increase the context length over RL loop to handle that.

**59:36** · In this particular case, they are basically putting this penalty function so that they can handle this part.

**59:43** · So, overall, what this showed was that when you started with GRPO on this AIME benchmark, if you put overlong filtering, you went from 30 to 36 on the quantity to be model.

**59:54** · If you did asymmetric clipping, you could go to 38.

**59:58** · With soft overlong punishment, you could go to 41.

**1:00:01** · And then with token level loss you go to 42.

**1:00:03** · And then if you do dynamic sampling, where you're basically doing a better distribution of rewards across the batch, you have a better signal propagation.

**1:00:12** · You basically go to 50, which was even better than what DeepSeeL-R1 distilled down to Qwen-32B had done.

**1:00:18** · So they could actually hill climb on the Qwen-32B themselves and get to a pretty strong score here.

**1:00:25** · So some of the learnings from this paper was that the loss function by itself was not a reasonable enough proxy.

**1:00:32** · When you're learning in RL.

**1:00:33** · You have to look at the response length.

**1:00:35** · You have to look at the entropy and keep it so that it's not too low but it's not too high either.

**1:00:40** · And then the percentage of samples that have a full accuracy of 1 tells you how much you need to sample.

**1:00:46** · So all three are important principles in learning in RL, and some of the challenges that you might have to look out for is that if you're a response length in the model outputs is exploding, then you have to control the loss there.

**1:01:01** · You have to control the entropy.

**1:01:02** · And then if you're not seeing improvement after a certain number of steps, then your reward model actually might be saturated.

**1:01:11** · So, effectively, what this is saying is that the optimization in the RL loop is harder.

**1:01:17** · So if I were to answer the question that was brought up earlier of SFT versus RL, RL does provide you in the domains where you do have a strong reward signal, it does provide you the ability to hill climb with fewer number of examples, but it does take a lot of work to get it right.

**1:01:33** · While supervised fine tuning oftentimes if you do have access to a lot of high-quality data, it's faster way to just improve the model performance in certain cases, but it doesn't bring reasoning capabilities or boost them in certain ways.

**1:01:49** · So if you were to compare the three different techniques that we talked about today.

**1:01:56** · So if you basically only had a few different examples like 100 examples with reasoning, and you are effectively just like playing around with a model, and you don't have RL infrastructure, STaR is a pretty good way for you to start getting the model to reason.

**1:02:12** · And simple reasoning tasks like GSM8K actually will see a reasonable amount of improvement there.

**1:02:18** · Maybe not phenomenal, but you're still staying within what the model was capable of.

**1:02:22** · If you go to DeepSeekMath and you use GRPO, you do need a good enough base model.

**1:02:28** · Plus, like you do need to prime the model with good instruction data.

**1:02:33** · But now you have a reasonably strong algorithm that can work even if you don't have enough memory-- you have a limited number of GPUs.

**1:02:42** · And then for standard math reasoning tasks, this was well proven.

**1:02:49** · And you need double kind of techniques when your reasoning chains will end up being longer, which typically correlates with harder problems.

**1:02:55** · So if your reasoning chains are going to be much longer, you need state-of-the-art performance, then you do need to control all of these variables in your RL algorithm and infrastructure.

**1:03:04** · But for competition-level problems like AIME and IMO this is very useful.

**1:03:12** · So what is it that we expect to improve?

**1:03:15** · All three techniques will improve, in general, the majority at K performance on the y-axis as you put more compute.

**1:03:22** · The answer formatting generally will improve as you apply these techniques.

**1:03:27** · And in general, the model will be more coherent over multiple steps.

**1:03:31** · But none of these will yet improve the fundamental capability, or just teach the model to solve new problems, or generalize a lot out of domain.

**1:03:39** · So there is some set of questions that are being asked at this point in time, what would it take for the last part to start improving?

**1:03:48** · Yes.

**1:03:49** · So I'm wondering whether \[INAUDIBLE\] you've just \[INAUDIBLE\] so hard like all right or all wrong, because this if you've done that part, that's like the only way you want that is on the \[INAUDIBLE\] So with that, it's \[INAUDIBLE\] I see.

**1:04:17** · I'm just wondering whether there's like-- That's not the reason.

**1:04:22** · I think the more fundamental question is that to.

**1:04:24** · Improve past K, you're basically improving the fundamental capability of the model to solve new problems.

**1:04:30** · So you want to see the model show capabilities in certain ways.

**1:04:35** · So typically, the fundamental capability scaling comes from-- the fundamental capability step jumps have typically been seen by either some sort of a breakthrough or by scaling in some dimension.

**1:04:48** · OK, so you see that this thing has a set of problems, always \[INAUDIBLE\].

**1:04:55** · Then it's possible that-- I'm not sure whether this is frankly true.

**1:05:00** · So you can answer the question.

**1:05:02** · Some other models can get the answer and then go back.

**1:05:07** · Let's take that one offline.

**1:05:11** · OK, so one of the things that I keep highlighting is something to keep in mind is that a lot of the RL loop or even the STaR method, like the quality of rationale, all of that depends on the ability of the model to reason or there needing to be some sort of a verifier or a reward model.

**1:05:29** · And the reward models if the model is too capable, then the reward rewards will get hacked.

**1:05:35** · And if the reward model doesn't have enough signal, then you're basically not able to hill climb the loop.

**1:05:40** · So it is a harder optimization problem in that respect.

**1:05:46** · Last lecture or last Friday, we looked at the autonomous coding applications where you do have access to verifiable rewards because you have-- like in math and code, you have the final correct answer.

**1:05:59** · Then you can also give execution feedback, which was the RL paper we looked at.

**1:06:03** · And then you also have unit test execution.

**1:06:06** · Similarly, there are some domains in which you have this kind of verification available, so it's easy for you to hill climb.

**1:06:13** · But then how many such places do you have this signal available?

**1:06:17** · These questions will continue to come up.

**1:06:18** · So what verification signals are good enough, and then there's, can you use an ensemble of verifiers instead of one single verifier to make up for the gaps of what a single verifier will provide signal on.

**1:06:32** · So all of these questions are extremely important.

**1:06:36** · So in terms of if you were to look at open problems in this domain, so, I think, this is still an active-- train-time scaling is an active area of research.

**1:06:45** · I already highlighted this.

**1:06:46** · There's a fundamental question of why only majority had K increases?

**1:06:50** · Why does Pass@K doesn't increase.

**1:06:53** · A second question is that we do see in the reasoning chains things like backtracking or the model is able to self-evaluate, self-correct.

**1:07:02** · We did show those examples early on, but are those behaviors real?

**1:07:06** · Like these reasoning behaviors are they emerging or were they already present and they're basically statistically becoming more prevalent?

**1:07:14** · And then a third bit right now is that we don't really have very good techniques to learn from failures.

**1:07:18** · There have been a few papers that have tried to learn from failures in useful ways, but currently, a lot of the techniques just filter them out.

**1:07:26** · Some promising directions that people continue to explore in this is along the data dimension of how do you generate better data to train the model?

**1:07:34** · Along the algorithm dimensions of like how do you get the reinforcement learning to be robust to noise in the reward models?

**1:07:41** · What kind of rewards should we use?

**1:07:43** · And then can you combine some of the rationalization techniques that we did with in STaR with, say, the techniques that we did in DAPO?

**1:07:51** · So all of those are very interesting directions that you could look into for your projects.

**1:07:58** · And with that, we have a few minutes left, but let's have questions.

**1:08:04** · For the new, big like out-of-the-box models that Anthropic and OpenAI are training, how much do you think they're still relying on just like common call like mixed token prediction, like raw text data like that they take from the internet or anywhere rather than instruction training data that they generate using reasoning techniques and techniques that we learned today?

**1:08:35** · What do you think is that fraction?

**1:08:37** · I see.

**1:08:38** · So I don't think that's published for Anthropic, but I think Grok was more public.

**1:08:43** · So, typically, the percentage of reinforcement learning versus pre-training has been closer to-- I think last year it was closer to say 99%, 1%, and then it's grown to perhaps like 5% or something like that.

**1:08:59** · Grok-4 claimed that it did 50% RL, but it actually did not quite improve.

**1:09:04** · Like 50% RL should give a big jump, but your bottleneck by a lot of the things that I'm showing you here of your rewards are not strong enough, or there is noise in rewards, all of those things are going to be bottlenecks.

**1:09:17** · So there is still a lot of open problems in this domain.

**1:09:21** · Yeah.

**1:09:23** · Let's see if there are more questions across the board, or is this lecture too complex for people to ask questions?

**1:09:31** · Too complex, OK.

**1:09:35** · Happy to answer questions after.

**1:09:43** · More questions across the class.

**1:09:45** · No?

**1:09:46** · I have a question.

**1:09:50** · You go back to the previous page.

**1:09:51** · You have \[INAUDIBLE\].

**1:09:59** · Is this something like if the model performed, oh, hey, this is calculus, and you help it to \[INAUDIBLE\] RL, and if the model never seen \[INAUDIBLE\] regardless how well it \[INAUDIBLE\], it can never infer either option.

**1:10:20** · Like Is that a fundamental reason?

**1:10:22** · Like \[INAUDIBLE\] is like fundamentally you think you need \[INAUDIBLE\] knowledge.

**1:10:27** · Mhm.

**1:10:28** · \[INAUDIBLE\] is like you \[INAUDIBLE\].

**1:10:31** · Exactly.

**1:10:32** · Yes.

**1:10:34** · OK, so maybe that's something like that's not the reason, \[INAUDIBLE\], because reinforcement learning is getting better at something you already can do.

**1:10:48** · Yeah, it's basically able to explore better in the design space of what it knows, and by exploration and search, it's able to arrive at the solution.

**1:10:59** · There was a question here, which I didn't let you ask.

**1:11:02** · All right.

**1:11:03** · Yeah, I was curious for especially on the directions of the-- so for very unique data set like AIME or \[INAUDIBLE\] where the number of data sets is very limited, how can we ensure that we have enough signals for verifiable rewards?

**1:11:22** · I mean, there's not enough data, but we need a lot of signal.

**1:11:25** · So how can you make sure that you have enough training and verification without accidentally leaking data?

**1:11:33** · So I mean, RL is more data efficient, so you do not need that much data to begin with.

**1:11:39** · So, I mean, like, that's why I was presenting these papers.

**1:11:41** · You do see that a certain number of enough examples is good enough to hill climb.

**1:11:49** · The verification signals are more a function of having good set of verifiers.

**1:11:53** · So I think it's already covered the ensemble verifier paper.

**1:11:56** · We already covered that.

**1:11:58** · So it's not just a matter of having a single verifier.

**1:12:00** · You can have multiple verifiers.

**1:12:03** · I see.

**1:12:04** · So when there's not enough data, we can just make up for that with many more verifiers?

**1:12:10** · So I think you solve the data problem separately.

**1:12:12** · But I don't think there are not enough data is the right abstraction.

**1:12:16** · I think it's do you have enough data to hill climb on is the right abstraction.

**1:12:23** · End up filtering out if you were doing dynamic sampling, for example.

**1:12:28** · OK, with that, we'll close the class, and I'm still around.

**1:12:31** · Thanks, everyone.
---
title: "Stanford CS329A Self-Improving AI Agents | Part 2 | Test-Time Compute Scaling"
source: "https://www.youtube.com/watch?v=-Ggc37xLj_Y&list=PLangBM27OtEA&index=2"
author:
  - "[[Stanford Online]]"
published: 2026-08-03
created: 2026-08-26
description: "Want to dive deeper? This curriculum is covered in the following online courses:- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html- XCS329 graduate course:"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=-Ggc37xLj_Y)

Want to dive deeper? This curriculum is covered in the following online courses:  
\- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html  
\- XCS329 graduate course: https://online.stanford.edu/courses/cs329a-self-improving-ai-agents  
  
A similar curriculum is covered in XCS329z https://online.stanford.edu/courses/cs329z-engineering-ai-agents  
  
Follow along with the course schedule and syllabus: https://cs329a.stanford.edu/  
  
View the course playlist: https://www.youtube.com/playlist?list=PLangBM27OtEA  
  
Video Summary:  
This lecture recording from Stanford's CS329A, Self-Improving AI Agents, delivered by Azalia Mirhoseini on September 26, 2025, examines test-time compute scaling as a way to improve model performance without additional training. It covers the Large Language Monkeys paper's finding that solve rate follows a power law as the number of parallel samples increases, driven by a long tail of hard problems each model solves only rarely, and it distinguishes majority voting from oracle verification to define the generation-verification gap. The lecture also covers a paper on optimally scaling test-time compute, which compares parallel sampling against sequential revision and introduces outcome and process reward models to guide search over candidate solutions. It closes with the Arkon paper on inference-time architecture search, which combines techniques including fusion, critic, ranker, and unit test generation across multiple models, reporting an average 14.1 percent improvement in pass-at-one accuracy over GPT-4 and Claude 3.5 Sonnet on reasoning, math, and coding tasks. Discussion throughout addresses when pre-training still outperforms added test-time compute for the hardest problems.  
  
Speaker Bio:  
Azalia Mirhoseini  
Assistant Professor of Computer Science, Stanford University  
  
Azalia Mirhoseini is a co-founder of Ricursive Intelligence, a frontier lab dedicated to recursive self-improvement through AI that designs the chips that fuel it. She is also an Assistant Professor of Computer Science at Stanford University where she directs Scaling Intelligence, a lab focused on developing scalable and self-improving AI systems and methodologies toward the goal of artificial general intelligence. Previously, she spent several years in industry AI labs, including Google Brain, Anthropic, and Google DeepMind, working on the development of Claude and Gemini. Her past work includes Mixture-of-Experts (MoE) neural architectures, now predominantly used in leading generative AI models; AlphaChip, a pioneering work on deep reinforcement learning for layout optimization used in the design of advanced chips like Google AI accelerators (TPUs) and data center CPUs; as well as pioneering research on LLM Test-Time Scaling. Her work has been recognized through the Okawa Research Grant, the Google ML and Systems Junior Faculty Award, MIT Technology Review's 35 Under 35 Award, the Best ECE Thesis Award at Rice University, publications in flagship venues such as Nature, and coverage by various media outlets, including WSJ, NYT, Forbes, MIT Technology Review, IEEE Spectrum, WIRED, and TechCrunch.

## Transcript

**0:05** · So today, we are going to talk about inference scaling.

**0:09** · We briefly hinted on this in the first lecture, so there are three stages for LLM kind of development.

**0:17** · The first one is pre-training.

**0:19** · This stage is historically takes a lot more time.

**0:22** · It could take several months.

**0:24** · A whole lot of GPUs that are used for training these.

**0:30** · And then there's the fine tuning step.

**0:32** · Usually, this is a less, or historically has been a less compute-intense process.

**0:39** · If you are talking about trillions of data, tokens in the pre-training side, on the fine tuning side, this is orders of magnitude less data that we use for fine tuning.

**0:50** · And then there is the inference part, where we get to use the model.

**0:54** · And we are going to see different ways that at inference time, we can make the model be better and become more useful without changing the parameters of the model and without any fine tuning of the models.

**1:11** · So let's first start with the Large Language Monkeys paper.

**1:16** · Again, you are familiar with the infinite monkey theorem by now because we discussed it on Monday.

**1:24** · But to recap, the idea of this paper is that we have an LLM and we have a problem as input.

**1:31** · Instead of generating the response for this problem only once, we are going to repeatedly ask the same input problem again and again.

**1:41** · This could be a number of times, it could be 10 times, 100 times, and so on, and we will see how that affects the performance.

**1:48** · And then we are going to have a verifier that can tell us which one of these responses were the correct response, and then that is going to be the output of this system.

**2:01** · The reason we like that is that by doing this repeated sampling, we can make models that are inferior.

**2:08** · For example, a Llama 3-8b or 70b that is not as capable as GPT-4o with single attempt.

**2:17** · But by doing this repeated sampling and selecting the correct one among the generated candidates, we can significantly improve the performance of these inferior models and make them better than these larger and proprietary ones.

**2:35** · And these are-- here you can see examples across a really hard math coding and different styles of math problem question answering problems.

**2:49** · Is this clear to everyone?

**2:52** · It just seems like the models and smaller models already know the answers to these hard problems, and just by doing this repeated sampling, we are eliciting and surfacing those answers.

**3:06** · It's just they just don't tell us that in the first trial.

**3:13** · Now, this paradigm of repeated sampling, works well across pretty much any domain that we have tried in so far, including agentic benchmarks such as SWE-bench, which mimics how a software engineer goes about editing code and creating new patches.

**3:36** · So here, we are seeing the coverage, meaning the fraction of problems that are solved by, at least, one of the samples.

**3:46** · And here on the x-axis, we have the number of samples going from 1 to 1,000.

**3:51** · And what we are seeing here is that a models such as DeepSeek can-- I believe this was the DeepSeek-V3 model can outperform models such as Claude 3.5 or o1 preview after 1,000 samples.

**4:12** · It can solve more coding and software engineering problems than those.

**4:16** · And the reason this is interesting is that, we are doing-- in this case for coding problems, if we have unit tests that we can use to select which one of these samples is correct, then we have an end-to-end automated way to create a more capable model, in this case, out of DeepSeek and open-source model.

**4:44** · Now, again, we saw pre-training scaling laws in the last class, and that was, we can predictably reduce the test laws given these equations in this paper.

**4:58** · And these equations might change given the setup, but there is a predictable path to increase data, amount of compute use, and the number of parameters in the model and use that to predict, or reduce the test laws.

**5:15** · So this is for pre-training, but it turns out, we can define a similar scaling laws, but this time for inference, or test time compute, and that is something that we showed in this paper.

**5:27** · Basically, we're showing that the relationship between coverage and the number of samples that are being drawn in parallel from the model follow an exponential power law.

**5:39** · So assume this says, coverage, meaning how many problems are solved by, at least, one of the samples, and then k is the number of samples.

**5:48** · And a and b are these kind of coefficients that we can find through the curve-fitting parameters that we can find through this scaling behavior of the model.

**6:03** · So concretely, as we scaled the number of samples across a range of models from Llama 3 8B, 7, 8B, and models like Gemma or Pythia.

**6:16** · And this is for various range of parameter sizes, going from 70 million parameters all the way to 70 billion parameters.

**6:25** · We can see that we can predict this power law and have a predicted curve that for the most part, very closely follows the actual practical coverage that we are seeing as we increase the number of samples.

**6:44** · So basically, the way to think about it is that we can predict to achieve a certain coverage, how many samples we are going to need and how much resources we should allocate to achieve that.

**7:06** · And again, these curves show that this behavior is true for a range of models and a range of parameter sizes.

**7:15** · Again, one of the very interesting properties that we saw here is that for a very small model, like a 70 million parameter, we also see this scaling behavior.

**7:26** · And, of course, this is true for much larger models as well, and it is true across domains.

**7:33** · Now, we looked a bit more into why we see this power law behavior in repeated sampling because it might be at first a little non-intuitive, because if the probability of the pass at one being correct,

**7:58** · the probability of a correct response to a question is, for example, p, then we can calculate the probability of, at least, one of the answers being correct at k for an individual problems.

**8:13** · So for a problem i, if we have the pass at one for problem i, we can calculate directly what is pass at k for problem i with this exponential equation.

**8:28** · I hope this is clear for everybody, but basically, this 1 minus p is the probability of the first k answers not being correct, and then 1 minus that is the probability of, at least, one of these k answers being correct, so this is for an individual problem.

**8:45** · But what we are seeing that across a suite of problems, we are seeing the power law, scaling law, meaning across these problems, we are seeing the equations are changing.

**9:02** · So the question that we wanted to answer is what behavior should we see across the problem examples in a data set that justifies our power law scaling laws?

**9:20** · And by looking into that further, what was observed is that in order to have the scaling laws that we observed, the sufficient and necessary condition for it is that we have a long tail of hard problems.

**9:42** · Basically, from a mathematical perspective, we are going to need that because this is the power law scaling, this is the per problem exponential scaling laws, and this is like this sort.

**9:55** · We need to have this curve for the past at one of problems in order to justify this power law scaling.

**10:05** · And empirically, when we looked into the problems, we saw that this condition holds.

**10:12** · And again, what this condition is is that we have a long tail of really hard problems on the most complex side of things.

**10:23** · For example, let's take a look at this model and the count of problems that are solved at pass at one and add more and more samples.

**10:36** · It seems like across all these problems, a large portion of problems are simpler and they're solved in pass at one.

**10:43** · And as we increase the complexity of the problems, where the pass at one probability is going to become lower and lower, we have a long tail of problems that have that property.

**10:56** · So these curves that you see here from high at simpler problems and low at harder and harder problems, meaning lower and lower paths at one is the type of problems, is the type of behavior that we are seeing across these tasks, and that is why we can see the scaling laws that we have observed.

**11:20** · Now, what this means for the science and the engineering around LLMs is that while previously companies would spend hundreds of millions of dollars, or billions of dollars on pre-training alone, and then a lot less on fine tuning and then almost like nothing at each inference call because it used to be like a one time back and forth between the user and the query and the model.

**11:53** · Now we have a new paradigm, where we can spend a whole lot more compute on inference, and use that to increase the capability of model.

**12:03** · And this compute the inference compute can be done offline.

**12:06** · We can release our agents to go solve a problem and just keep generating tokens and keep improving the quality of the answers that they generate.

**12:20** · Now, when we talk about this repeated sampling, something that's important to have in mind is the need for automated verification because if you have a bunch of samples, we still need to know which one of them are the correct ones and how to go about selecting that.

**12:43** · In certain domains, verification is easier than the others.

**12:48** · For example, for certain types of math problems, you can use formal proofs.

**12:55** · So given a proof, the strategy, we can run them by these formal proof software tools to verify whether each step is correct or not.

**13:06** · We can write unit tests for coding.

**13:09** · And in some cases, writing a unit test arguably, arguably, is a much simpler task than writing the entire program that solves a problem, so the unit test can be written, for example, by humans, and we can use that as our verifier.

**13:29** · There are other cases like AI as a compiler, and this is one of the projects in the lab and the direction that I'm very excited about, and that is when we can generate compiler lower level code, like CUDA for a source code like PyTorch with LLM.

**13:48** · And the reason this is verifiable is that, for example here, we can always compare the output of CUDA with the source PyTorch and see if they're the same for any given input.

**14:04** · So we don't need if we want to say whether the model has generated the correct CUDA code for our source PyTorch code, we can just see whether their outputs match for any inputs.

**14:21** · For those of you who are not familiar CUDA, I hope you all are, but it's a lower level language for writing more hardware aware and optimized for hardware code on GPUs.

**14:38** · For example, here, we have a data set, or benchmark on CUDA generation called KernelBench.

**14:47** · And here, again, we are seeing the same linear improving coverage in this case for CUDA code generation as we increase the number of samples that we take from the model.

**15:00** · And in this case, we have this, again, by default, perfect verifier that we can use for measuring the correctness of our CUDA generated code.

**15:13** · And there are other examples of this.

**15:18** · Basically, any kind of translation between two languages.

**15:21** · If you want to port from Python, or C++ to Java, or vice versa, again, this is true.

**15:28** · You can measure the equivalency much easier.

**15:34** · Now there are domains that we don't have verifier for.

**15:38** · And in those domains, what we observe is that there is a large gap between best of n methods such as majority vote voting and model-based rankers and what is the true coverage of the model.

**15:54** · Let's take a look at one example here.

**15:58** · So here, we compared a few different methods.

**16:01** · We are going to learn about reward models or verifiers on Monday more, but let's take a look at these examples.

**16:08** · So we have a number of samples, and then we are measuring the success rate here, like basically what would be the output of this system?

**16:17** · Majority voting, or the green one is we just see which answer among the generated answers has appeared the most, so based on that, we just select that answer or that response as the output of our system.

**16:33** · Does that make sense?

**16:34** · It's just majority voting.

**16:36** · And the blue line here is coverage.

**16:39** · This is assuming we had a perfect selector, or verifier in this case.

**16:44** · And as you can see here, there is a large difference between majority voting, which plateaus after 10 or 50 samples, and what we could possibly get if we had a perfect verifier, so this is a very, very large gap.

**17:01** · Especially, and this gap is even more pronounced if you have harder problems.

**17:06** · So for example, the capital MATH here, data set is a harder, more complex data set than GSM8K And here, we compared other methods like using a reward model that measures, gives a reward per answer, and we take the best of those, or ways to combine these tools.

**17:31** · We will learn more about these reward models.

**17:34** · Basically, they're LLM-based LLMs that are trained to score the response quality.

**17:44** · And even with those, there is a large gap.

**17:47** · And this is what we call the generation verification gap.

**17:52** · So the generation, it turns out, we can generate a lot of good responses, but the verification is basically this gap.

**18:01** · This tells us how much we can actually capture those responses or those correct answers.

**18:09** · The reason methods such as majority voting doesn't work is that, as we look into the quality of answers, it turns out that for some problems that are hardest to solve, sometimes we see that they're solved maybe even once, or two times, or three times across the 1,000 or 10,000 samples that we take from the model.

**18:34** · So these correct problems are actually very rarely solved by the model with the samples that we are taking from it, so it makes sense that a majority voting mechanism cannot capture those because they're rare.

**18:51** · But for many of the problems in this case, especially for the GSM8K, which is simpler because the answers, or responses are simpler to generate, majority voting works for many of the problems, but even in this case, for some of the hardest problems, the frequency of correct answers actually pretty low.

**19:14** · So that makes it harder from a verification perspective how do you find them?

**19:18** · How do you find that which ones are correct?

**19:22** · Now, I want you to-- here are some discussion questions that I want to put it here for something like two minutes or so, and I want you to think about it.

**19:35** · And hopefully, we'll have some volunteers and volunteer some of you to answer some of them.

**19:46** · So two minutes for this.

**19:48** · Maybe we talk after.

**19:52** · \[SIDE CONVERSATION\] OK, let's get back.

**19:57** · Who wants to answer question 1?

**20:01** · I'm very interested in how you would build on this, if you were to do some research here, or what takeaways you got from these papers.

**20:17** · Anyone?

**20:21** · Yes.

**20:22** · One takeaway is that sampling any answers and issues.

**20:31** · If you have a good verifier, it's greatly helps with your accuracy.

**20:36** · And the second takeaway is that the quality of the verifier is very important in this approach.

**20:44** · That's right.

**20:49** · Anything else?

**20:51** · Yes.

**20:52** · \[INAUDIBLE\] it is possible to write a model to \[INAUDIBLE\] that way make examples.

**20:59** · For example, like the model \[INAUDIBLE\] descriptions and the model for the solution that is a \[INAUDIBLE\] even if you're not sure the solution is right.

**21:16** · Are you talking about revising a solution-- Yeah.

**21:20** · --by next round?

**21:22** · We're going to hear about it in a minute.

**21:25** · Sounds good.

**21:26** · Yes.

**21:27** · I'm looking at it two directions.

**21:29** · One is the \[INAUDIBLE\] and accuracy.

**21:32** · And for that, I would look at a hybrid approach, where I would develop a knowledge graph along with advanced documentation.

**21:42** · And then any returns to the rank method.

**21:45** · When \[INAUDIBLE\] comes time the score is lesser on the accuracy and more or less rely on the knowledge to give me more accurate answers, that way you can increase the speed in the answer while \[INAUDIBLE\].

**22:01** · So you're suggesting use RAC to boost or compare?

**22:08** · With the knowledge first, and then only when they feel that the accuracy is not coming up to the mark, we go through the right documentation because that also lowers the time, and there is-- So you're asking that can help with efficiency in the time domain?

**22:25** · Is trying to reduce the dependency and damage to increase the accuracy and precision.

**22:33** · One more.

**22:34** · Maybe you were waiting.

**22:36** · Yeah, so something that I've thought about also is just-- and even if it's easy to medium level of difficulty with respect to verification or verifiable domains, it would be cool to see how pass at k changes with respect to k, when we employ initial search techniques, almost like a self-study approach.

**23:02** · If there's some way to maybe consolidate, let's let the model explore this domain, gather insights as if we're not asking it to sample any solutions yet.

**23:12** · And maybe that can give way to some output context, and we could then funnel into parallel sampling.

**23:17** · We might see maybe better trends with respect-- Absolutely.

**23:21** · And we're going to learn about some of them.

**23:22** · There are ways to improve test time scaling beyond just repeated sampling, including self-study, search, and tool use.

**23:31** · Maybe one more.

**23:34** · Yes.

**23:36** · Well, one interesting extension might be to \[INAUDIBLE\] verifiers.

**23:41** · Without a good verifier, then the best you can do is \[INAUDIBLE\] what you showed in the previous slide, which usually doesn't work very well for hard problems.

**23:50** · But maybe there are some problems, where it's hard to verify the answer is correct because it's too expensive, or it's just too hard naturally, but it's easy to find an answer wrong, so you can project like bad answers.

**24:06** · Maybe that would be more obvious in terms of testing.

**24:08** · And then you can just keep \[INAUDIBLE\] something \[INAUDIBLE\].

**24:13** · So one interesting direction would be trying to look at different domains, where there is much difficulty.

**24:21** · And also maybe verification is not fully accurate, or maybe it's a bit lost, but verify it's its own model because it's a simulation.

**24:28** · It's like a physics, or a molecular dynamics simulation, or something, and then how you would deal with that.

**24:34** · Basically, there are other ways to filter out the incorrect answers.

**24:39** · Maybe use a simulation, or some other tool use, or another model to do that, depending on the domain.

**24:49** · So all of the data set here, the 10,000 different samples per problem is available on Hugging Face.

**24:57** · If anybody is interested to go around how to shrink that generation verification gap, that could be potentially a good research project for the course.

**25:10** · Yes, last question.

**25:12** · Yeah.

**25:13** · Can one try to generate multiple verifiers like maybe generate 10,000 verifiers and then do majority voting on the result of the bad verifiers?

**25:24** · Yes.

**25:25** · That's also a very interesting research question.

**25:28** · So on Monday, we're going to learn about this weaver, which is a work that we've done on ensembling, but a week supervised ensembling of verifiers.

**25:37** · We don't have 1,000 of them, but we can have 10 or 20 of them, but that direction is definitely also interesting.

**25:44** · It's very costly, though, from a compute perspective.

**25:47** · Maybe we should move on to the-- any other about the other two questions, anything?

**25:54** · We discussed some of it in our discussion, but anything that you want to share last minute?

**26:00** · Yes.

**26:01** · What is up with the investigated whether the coverage number is real, like software engineering tasks, for example?

**26:08** · Or could you pass the test cases, but it's actually about \[INAUDIBLE\]?

**26:12** · For example, for the math problems, we manually looked into the answered questions, and it was something above like a 90s, 7%, 8% by manually checking that, but that's also always a case for failure mode, if your unit tests don't have true coverage of the code, so the quality of the verifier matters.

**26:37** · Yes.

**26:38** · Maybe it's moved up to be able to generate \[INAUDIBLE\], so you're verifying each node?

**26:45** · Yeah, let's talk about that and what's coming next and how we can make different ways of test time scaling.

**26:55** · So with the monkeys framework, we saw that repeated sampling is effective, but there are other ways to scale sampling.

**27:04** · And let's take a look at this paper.

**27:06** · Scaling LLM test time compute optimally can be more effective than scaling model parameters.

**27:12** · We going to touch on certain aspects of it that is most relevant to test time scaling, so there are two ways.

**27:20** · Parallel sampling is one way for us to generate multiple answers per input question.

**27:27** · But there is another way to generate, or generate answers, or use test time scaling to improve the quality, and that is when we do sequential revisions.

**27:38** · For example, the model comes up with one initial steps of the problem, or one initial approach for solving the problem, and it keeps revising that, or it keeps improving and adding to that.

**27:52** · And that is the sequential approach, so instead of asking the model multiple times, we let the model know that it can keep revising its answers, look into that from a different angles, and continue doing so until it's confident that it's ready to generate an answer and then finally output that.

**28:12** · Yes.

**28:12** · So is this by our own prompting or is it the models?

**28:17** · In this case, let's assume by our own prompting, but when you look at the reasoning models, they are now trained.

**28:24** · Internally, we see this kind of behavior in them, so they do this revisions sometimes in their own answers.

**28:35** · Now, there is another way to scale test time compute, and that is how we select the answers.

**28:43** · So for the parallel sampling, we looked into the outcome like there are n different responses.

**28:50** · We look into the outcome and see if they're correct or not.

**28:53** · We mentioned unit tests and so on, but there's also this other way of learning based, or outcome reward models, where they look into the outcome and say whether they're correct or not.

**29:06** · Of course, their accuracy, or quality can be limited, especially if we go to new domains.

**29:12** · But outcome-based reward model is another way that they look into the final answer and they generate a score.

**29:19** · Basically, these models are trained to give a reward based on an output.

**29:25** · Then there is also the process reward models.

**29:28** · So the difference between process and outcome is that process reward models are designed to give a score per step of the generated solution.

**29:38** · For example, we have a math problems, there are five steps that the model takes before generating a solution.

**29:48** · Process reward models, again, we learn about this more on Monday, I believe, are trained to give a score for the steps of the generation.

**29:58** · So that's the difference between the two.

**30:02** · Now, for best of n sampling with a verifier, again, the problem is easy.

**30:06** · We generate parallel samples, and then we can use an outcome-based reward model to see which one has the highest score and then take that as our answer.

**30:20** · Then there are other ways that we can bring these reward models into the processing, into our test time scaling framework.

**30:30** · For example, here, let's assume at each level of answering this question, we have a budget of four samples.

**30:40** · We take these four samples, and then here, use a Process Reward Model or PRM to in this case, we select the top two with the highest score from our PRM.

**30:53** · Then again, we sample from them and we continue.

**31:00** · And we can have a threshold for selecting the top two kind of responses in this case and expanding the tree from there.

**31:12** · So here, we are doing a beam search approach that uses the process reward model to guide how we are sampling our model.

**31:21** · Is that clear?

**31:24** · Yes.

**31:25** · How do you choose the options?

**31:27** · Based on the PRM score.

**31:28** · So the process reward model is trained to generate a score imagine between 0 and 1 based on the step given the question, and/or just the step alone.

**31:44** · Is the PRM fine tuned for that?

**31:47** · Yes, PRMs are generally also fine tuned from language model.

**31:51** · As you can imagine, they would work better for in-domain types of tasks, so if you have a certain benchmark that you want to optimize for, of course, training a PRM on a subset of that task helps you with test time scaling on that task better than across new task.

**32:12** · But because they're language model based, they do exhibit some generalization across tasks as well.

**32:19** · Yes.

**32:21** · For the process reward, is this a reward that's being computed in practice?

**32:27** · I don't know what the research is per token that is being done, or maybe blocks of tokens and then it's being computed.

**32:34** · Yes.

**32:35** · It's not per token.

**32:36** · It's per step.

**32:39** · And this is something we're going to learn about in future lectures.

**32:42** · Imagine, these are like a math problem, and then there are steps to answer that.

**32:48** · One way to do it is to have humans annotate the quality of each step like yes or no, this is good or bad, and then training the model based on each step, which could be like you can assume it's like one intellectually meaningful chunk of the result, or it could be you can define it as a sentence and so on.

**33:13** · And, of course, as it's very intuitive, if you combine the two of outcome based reward model and parallel based upon sequential revisions, you get better results.

**33:27** · This field is still there's a lot of unknown questions around this, but combining the two.

**33:36** · For example, one simple way to combine that is instead of one sample and revisions, you do two and you get to two final answers, and then you use the best one, either using your PRM or ORM to select how the two are.

**33:57** · But you're augmenting each parallel sample with these sequential revisions, and you can use a PRM to guide that search for each sequential revision.

**34:08** · Something that's interesting is that the PRM, there are many off the shelf PRM's that you can use for your tasks.

**34:16** · So you can go and say, take a pre-trained PRM and use that to guide the search for your own task.

**34:22** · And you can potentially find a PRM that is most relevant to the type of task that you're doing, and you want to do test time scaling on, or you can train your own PRM and ORM based on your own data as well.

**34:40** · So this paper looked into the math data set and something like 12k train set 500 test questions, used the palm model.

**34:51** · And what was interesting here is that they defined a notion of difficulty for measuring these different scaling behaviors, and for that, they looked into the pass at one performance of the model on each problem.

**35:08** · And by just measuring that, they define OK, these are the problems that are hard, these are the problems based on how many of the generated answers are correct across a body of a number of samples.

**35:20** · They had five different bins for the complexity of the problem, and they did that, as we see to get some conclusion about what test time scaling works better for harder or easier task.

**35:36** · They also train their own process reward model, and even they fine tune a model for creating these revisions.

**35:43** · But right now, every model that we use pretty much it's capable.

**35:48** · It's just as long as it's instruction-tuned, is capable of doing revisions, if you ask the model to do so.

**35:57** · And there are some interesting observations here.

**36:00** · For example, here is the majority voting for these problems.

**36:05** · The accuracy as the generation budget increases, and then the purple one is the ORM one.

**36:14** · And the green one is the PRM one, and then the blue one, if you really try to optimize different ways of mixing and matching things.

**36:27** · And this area is the one that still is an open research like how do we do that?

**36:33** · How do we go about mixing and matching revisions and parallel scaling to optimize the test time scaling because at the end of the day, we want for each accuracy, we want the minimum generation budget to hit that accuracy?

**36:49** · And in a few slides ahead, we talk about one method to optimize this scaling and budget performance per budget.

**37:00** · They also looked into these different bins of difficulty, so number 5 is the most difficult questions because the accuracy is the lowest and number 1.

**37:09** · And then here on the right, there's these colors is the sequential to parallel ratio.

**37:16** · And while they're saying that OK for the easier problems, it seems like this darkest the darkest purple color achieves highest accuracy, and that's where we have a lot more sequential tokens compared to parallel.

**37:34** · When the problems are more difficult, and to some extent, those are some of the more interesting problems, this optimality is harder to say.

**37:42** · It's harder to say whether it's sequential or the ratio changes even from bucket four to bucket five on how you should allocate that.

**37:57** · Another observation from this paper was that-- and this is still a work in progress, and I believe still the true observation as of today is that for easy and medium questions, it seems like additional test time compute can be more favorable than scaling pre-training of the model.

**38:21** · So here, we have these two.

**38:24** · The easy are the green, medium is blue, and orange is the hard questions.

**38:31** · It seems if we look into the ratio of inference tokens to pre-training tokens, it is positive for the easy and medium problem, but for the hardest problem, it seems larger models like a more pre-training, or larger models still do better if you are from a tokens optimized perspective.

**39:01** · And this is something that we have seen in many of our research in the lab or around the lab as well.

**39:09** · It seems like models, simpler open source models, or smaller models are becoming more and more useful as we take more test time compute, apply more test time compute on them.

**39:22** · But still, for the very, very hard problems, still the frontier models, which presumably use more pre-training and they are larger, they do better even if we had a whole lot like infinite budget for test time scaling.

**39:36** · Of course, we don't have infinite budget, but any reasonably large test time scale.

**39:41** · Yes.

**39:42** · In this case, how do you inference for this pre-training?

**39:46** · Because it seems like for inference, you use it much like \[INAUDIBLE\], whereas for pre-training tokens, it's you use it once and you can use it twice.

**39:54** · Yes, that is true.

**39:56** · But in general, from a-- but this is still-- so basically, yes, pre-training is done once, but scaling is every time we run the model.

**40:17** · But still, this is an interesting observation from the perspective of, are we done doing pre-training because we can just keep sampling from the models we have, or no, pre-training is still helpful and we should do more and more?

**40:34** · Not everyone can pre-train a large model.

**40:38** · So even if pre-training was better than test time scaling in any scale, not everyone can do that because it's a very expensive process.

**40:49** · So this is very interesting that for many problems, we can do test time scaling, even if we do it every time for a new problem, because that's feasible.

**40:59** · But also, on the other hand, for the hardest problems, we still need to do pre-training, and better models still do better.

**41:07** · That makes sense.

**41:07** · I was just curious precisely in the graph when it says like the ratio is 1 for retraining of, for instance, retraining.

**41:15** · Does that mean that it's \[INAUDIBLE\] training, there was also one training used for a single task?

**41:23** · No.

**41:23** · No, it's not exactly that.

**41:25** · It's more like some ratio of pre-training to inference compute.

**41:29** · It's not a one-to-one because it doesn't make sense in that case.

**41:34** · My question is, why is it that those larger models still count better?

**41:40** · Can we take a smaller model and yet make it an expert on hot questions?

**41:45** · You can always fine tune a model to become better on a certain set of questions, but we are talking about a more general perspective of let's have a whole lot of data that's general, not specific to a specific task and just compare the common recipes that we use for training models.

**42:10** · Let's just follow that and then see how much they do better at test time.

**42:22** · Any other questions?

**42:25** · So maybe we discussed some of these already, but here are some more questions that I give you another two minutes, let me check the time.

**42:36** · Yes, we do have time, to think about this.

**42:41** · This helps you absorb some of the topics that we learned, or heard about in the previous slides, and then we discuss them in two minutes.

**42:56** · OK, should we start?

**42:59** · Anyone wants to add any comments here, or any questions you might have?

**43:06** · Yes.

**43:07** · So do you try sequential and try too-- what about tree search?

**43:12** · And in that case, you're doing the-- You're mixing the both.

**43:17** · Yeah, you're kind of mixing, right?

**43:19** · Yeah.

**43:19** · There is no universal answer that can be there.

**43:22** · But the general sentiment was that does better, like some sort of combining the two than doing-- \[INAUDIBLE\] you do, so reduce a lot of the compute that you're doing or reuse \[INAUDIBLE\] that you're doing because it's a tree-- Yes, yes.

**43:39** · That is when we discussed the beam search stuff and the PRM, like bringing a PRM to cut the tree at each level and explore only the more promising branches.

**43:57** · Anything else?

**43:58** · Yes.

**43:59** · \[INAUDIBLE\] as the thinking that that's the easier problem, the more perhaps you have towards the success of solving it.

**44:09** · Therefore, it could be more sequential \[INAUDIBLE\] problem because you would-- there are few students solving, so you would need many parallel process to find at least one viable solution.

**44:22** · And we started thinking a little bit also like to do this in a chain of thoughts kind of way, where you are doing a chain of thought, but verifying through all the steps into our chain of thoughts instead, and then pruning from these branches that are violating anything.

**44:37** · Yeah.

**44:38** · So in terms of sequential, you're saying that for easier ones, easier problems-- for harder problems, you mean you need more exploration potentially for easier-- To the correct answer.

**44:51** · Or for easier problems, because like any kind of path might lead us to the correct answer, we might not need to explore different parallel solutions.

**45:03** · Yeah, that is an intuitive kind of way of thinking about this.

**45:10** · Any other thoughts?

**45:19** · In general, this is a very interesting kind of problem to think about.

**45:23** · How do you-- let's assume that these tokens that you generate is like a knob that you have to increase problem, the quality of the responses, how do you allocate this knob?

**45:34** · And how do you elicit these generations from the model?

**45:38** · So let's think about in the following, I'm going to talk about one way to optimize these kind of test time scaling to generate optimized answers.

**45:47** · And that is the Archon paper, an architecture search framework for inference time scaling.

**45:55** · So the problem state-- and your TA is one of the co-authors of this work.

**46:00** · So the problem in this paper is that, again, we are interested to see how we can mix and match different inference time scaling methods to build the optimize the frontier of capability or correctness versus cost.

**46:18** · And the other thing that-- again, all of these questions basically saying the same thing that how we can optimize assigning inference compute two different tasks.

**46:32** · And basically, design mechanisms that gets us to the high quality answers while not wasting too many tokens and generations.

**46:43** · So here is the arc-- like in this case, we thought of inference scaling in this project as an inference architecture design problem.

**46:56** · So here is how the Archon framework works.

**47:00** · On the input side, we had a set of target benchmarks that we wanted to get good results on these benchmarks.

**47:06** · So these are the benchmarks we are optimizing for.

**47:09** · There is an inference called budget.

**47:11** · And then there's also a set of available LLMs, because we can always mix and match different models also to get to a correct answer for a input question.

**47:23** · And then we have a set of inference time techniques, which I'm going to describe in the following slides.

**47:29** · And then we designed this optimizer.

**47:33** · It's called itest.

**47:35** · It's inference time architecture search that basically tells us how to put together these different models and different inference time techniques together, whether it's parallel sampling, sequential, and all that, in order to get high-quality results given the budget, the inference called budget that we have-- how to optimize the quality of results based on that.

**48:00** · And then the output is this architecture that mixes and matches these different techniques and models together.

**48:08** · So let's take a look at different inference time operations.

**48:12** · So first, we have the general-- we call it the generation, but this is basically just sampling from the model.

**48:24** · And this can be part of the repeated sampling approach.

**48:28** · So if we generate n-- we use n generations at a time, that means we have generated n different responses to our input question.

**48:38** · So that's one type of inference time scaling.

**48:41** · Another one is fusion, which was surprisingly a very effective method.

**48:46** · So fusion is, let's say, we have K different responses, and we want to generate one output response out of these K. Fusion takes an LLM and asks an LLM the same exact question that I just said.

**49:06** · Basically, it says, here's the input question.

**49:09** · Here are K different responses to this input question.

**49:13** · Given all of this, generate or synthesize one output response for the input question.

**49:21** · Basically, we are showing all of the K generations to the model, such that the LLM can generate an output answer while being aware of all the possible ways that this question is answered.

**49:38** · And this is-- it goes under the category of sequential update.

**49:44** · We have this parallel samples, but then we are kind of fusing them into one answer.

**49:49** · Then there is the critic, which basically, for any given response, we can ask a model to generate or describe the weaknesses or strengths of these response.

**50:06** · And that could be one kind of inference scaling action.

**50:12** · And then we have the ranker.

**50:14** · This is-- again, these are all prompting based optimization for the model.

**50:18** · We haven't trained the model to do this specific test time scaling task.

**50:22** · We just ask the model in the instruction prompt that, can you rank these generated responses from the previous step based on their quality?

**50:38** · And then the verifiers generates the-- returns the response while also talk about the reasoning of why it came to this kind of way to score a certain answer.

**50:52** · I'll get to the next two unit tests generation and evaluation in a bit.

**50:57** · But just to show you how effective these different inference time scaling techniques are, let's take a look at this win rate for what tasks-- we don't have the task here.

**51:15** · But it's one of the task of one of these benchmarks that I don't know if you remember the task.

**51:23** · Yeah.

**51:26** · Some question answering reasoning benchmark.

**51:31** · So here, let's take a look at how these things work.

**51:34** · So first, we have-- let's say, we have a number of repeated samples from the model.

**51:41** · It goes from 1 to 10 on the left side.

**51:44** · Let's focus on the graph on the left side.

**51:46** · And then the orange one is the kind of worst possible way of approaching it.

**51:52** · We just randomly select one and look at the quality and the correctness of this response.

**51:59** · The green one is when we use the model to rank them, to rank the responses, and we select the top one ranked by the model and report that.

**52:13** · That already does better than the orange one.

**52:16** · The blue one is Oracle selection, meaning let's assume we are not mixing these responses in any way.

**52:26** · We just select the best one generated.

**52:30** · Let's say, we have an Oracle verifier that can tell us which one of these is correct.

**52:34** · And that obviously does better than just asking the model to rank them because it's an Oracle verifier.

**52:41** · And then we get to the red one, which is where when we use the fusion.

**52:46** · So basically, for each point here, let's say, we are at 5, the red data point is basically we have given these five responses to the model and ask the model to synthesize one answer, one final answer, given all this information.

**53:03** · And it's so interesting, and this paradigm is so powerful that that can on its own improve the quality of responses over Oracle selection.

**53:15** · And then finally, the purple one is where we-- instead of fusing all the responses, we first selected the top five, and then we went about fusing them.

**53:34** · So it seems like some sort of a filtering of the two does better.

**53:41** · Now on the right side, we are doing a different experiment, and that is we are-- on the left side.

**53:48** · We had only one model generating everything.

**53:50** · On the left side, we had-- we were using-- we were adding models.

**53:54** · So first one is just one model generating one answer, two the baseline is two different models generating one answer, and 10 is 10 different models, each generating one answer.

**54:05** · And we see that, of course, the random result becomes worse because the model we looked on the left was I think it was among the better models in this ensemble.

**54:17** · But we still see the same trend, even if these responses are coming from different models, basically the same trend of how these all follow each other.

**54:29** · Yes.

**54:30** · Which model is fusing?

**54:32** · If you're using 10 different models, you're asking somebody else to rank or fuse your-- I think it's the model number one in this case, the same \[INAUDIBLE\] that was in all of those.

**54:43** · And this was the way we created the ensemble was first with the best model and then added the second best model and so on.

**54:56** · Now let's take a look at a couple other inference time techniques.

**55:01** · And that is unit test generation and evaluation.

**55:04** · I think one of you was mentioning something like this earlier as well, that where we can ask the model to generate these unit tests, say when it gets to coding task or math, math problem-solving or other reasoning tasks.

**55:22** · And the unit test evaluation is even crazier.

**55:24** · Like instead of running the unit test, you're asking the model to evaluate a generated answer against a unit test.

**55:36** · For example, here is a prompt check for-- so the coding problem in this case is check for balanceness of round brackets in an input string.

**55:47** · That's a coding question.

**55:49** · And then here is an example input.

**55:51** · Here is the type of unit test that the model could generate.

**55:56** · For example, given a string with an odd number of brackets, the solution should output no, which is like a good unit test in this case.

**56:04** · Another one is when a closing bracket is encountered, it must match the most recently open brackets that hasn't been matched yet.

**56:12** · That's another kind of reasonable unit test.

**56:15** · And then you can ask the model to actually generate the code to test this as well.

**56:20** · Now let's take a look at the types.

**56:22** · I don't know if you guys see this well but the type.

**56:25** · But this is so big, there's no way for me to put it here with large font.

**56:30** · But this is the type of architectures that Archon found.

**56:34** · So basically now think about it this way.

**56:37** · We have different ways of mixing and matching models and inference time techniques, and we can define these layers of optimization.

**56:45** · For example, the first layer in this case is generation.

**56:48** · And then these generations are from different models in this case.

**56:52** · And then we have a critic and a ranker.

**56:56** · So basically, the critic will criticize these generations and then we rank them and then be the optimizer found that we could have a bunch of users at this point, like each fuses these responses into one output.

**57:13** · And then we can go from there, continue this critique ranker.

**57:19** · And this was like a rather complicated architecture.

**57:21** · And the way that we optimize this architecture is that we did some kind of pre-processing to reduce the space of optimization.

**57:32** · For example, the fact that we found this sequence of generation critic ranker and user do really well.

**57:39** · We did that offline, so we limited the search space just because doing this search is very expensive.

**57:46** · We need to run a lot of inference calls.

**57:48** · But then the way we optimize it that we had a held out data set that-- we had a training data set that we could optimize against that and create this accuracy versus the number of calls that we are making to these models, kind of as a metric that we are optimizing against.

**58:07** · We want to maximize accuracy.

**58:09** · And for any given budget, inference budget that we have.

**58:16** · And this is for some of the coding problems.

**58:19** · This was an optimized architecture.

**58:21** · Basically, we generate a ton of samples.

**58:24** · We generate unit tests and then we evaluate them.

**58:28** · Now, an interesting property here is that we found that stacking more and more layers of these inference time techniques, or making it deep in a way, actually does help with our accuracy.

**58:49** · In this case, for example, the right most pink graph is where we have an ensemble, meaning we have different models in our loop.

**58:59** · And we have three layers of critiques and fusers and a final fuser layer.

**59:06** · And this is significantly better across many of these tasks over both just using a simple the best model only once, or the best model eight times with one layer of fusion.

**59:19** · So it seems like these additional layers that we are adding here is actually-- just like in deep learning, we are adding layers in pre-training and the model gets better.

**59:28** · Seems like these careful kind of additions of these inference layers are helping the model become more and more accurate.

**59:35** · Across many of the tasks this is true.

**59:40** · And so now the optimizer itself, we used an Bayesian optimizer again to simplify the search space.

**59:48** · We did a few things.

**59:50** · For example, we limited the optimizer to only use one inference time technique per layer, and the first layer was always just the generator.

**1:00:00** · And then we had this cascade of ranker, critic, verifier.

**1:00:06** · They could go anywhere, but we made certain kind of modifications to the search space.

**1:00:12** · For example, a critic should go before a ranker or a fuser always because we did some testing locally and saw this is a better choice.

**1:00:22** · And then a unit test generator must be followed by an evaluator up.

**1:00:27** · And again, we use a Bayesian optimizer to do this.

**1:00:32** · This is often a very powerful methodology, a ton of good open source software to do Bayesian optimization for you.

**1:00:43** · Basically, you have this search space that you want to configure it with different kind of choices for the architecture.

**1:00:51** · And the output side, you have the accuracy and you want to optimize for that.

**1:00:55** · And this does better than greedy search or random selection.

**1:00:59** · We are much more sample efficient in terms of number of configurations that Archon searches until it reaches a final kind of architecture, and we can define different objectives for it.

**1:01:12** · For example, available models, inference time, inference, core budget is one of them or some of them.

**1:01:22** · The thing that I want you to pay attention to in this graph is that this interesting property that Archon is, at the end, generating one response at the very end.

**1:01:32** · So it's like you're optimizing paths at one at the very end.

**1:01:36** · And what was interesting here is that while using just the open source models, we could match or exceed these closed source models at the time, the frontier closed source model at the time, by a large margin across many of these tasks in terms of paths at one.

**1:01:59** · Here's the average path at one improvement.

**1:02:02** · And not only that, we could train Archon to be task specific.

**1:02:06** · So when we are doing the Bayesian optimization, we only look into a certain task and we test on that, or we could train Archon to be general purpose.

**1:02:17** · So we wanted it to do better good across many-- to do well across many tasks.

**1:02:23** · And even that the general purpose one does really, really well and better than the frontier models across these tasks.

**1:02:31** · And that was a very interesting observation that you can design these inference time architectures that do well beyond the task or the limited tasks that they're trained on.

**1:02:44** · So on average, in this case, we were outperforming GPT-4.0 or Claude 3.5 Sonnet in passage one by an average of 14.1% across these instruction following reasoning and math encoding problems.

**1:03:00** · Here are some questions, that I want you to think about.

**1:03:05** · But since we're out of time.

**1:03:07** · Hopefully, you think about it yourself.

**1:03:11** · And hope you have a happy weekend.
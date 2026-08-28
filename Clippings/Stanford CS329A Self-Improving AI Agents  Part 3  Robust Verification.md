---
title: "Stanford CS329A Self-Improving AI Agents | Part 3 | Robust Verification"
source: "https://www.youtube.com/watch?v=p7TdPUcPoik&list=PLangBM27OtEA&index=3"
author:
  - "[[Stanford Online]]"
published: 2026-08-03
created: 2026-08-26
description: "Want to dive deeper? This curriculum is covered in the following online courses:- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html- XCS329 graduate course:"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=p7TdPUcPoik)

Want to dive deeper? This curriculum is covered in the following online courses:  
\- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html  
\- XCS329 graduate course: https://online.stanford.edu/courses/cs329a-self-improving-ai-agents  
  
A similar curriculum is covered in XCS329z https://online.stanford.edu/courses/cs329z-engineering-ai-agents  
  
Follow along with the course schedule and syllabus: https://cs329a.stanford.edu/  
  
View the course playlist: https://www.youtube.com/playlist?list=PLangBM27OtEA  
  
Video Summary:  
This lecture recording from Stanford's CS329A, Self-Improving AI Agents, taught by Azalia Mirhoseini on September 29, 2025, traces the evolution of verification methods for large language model outputs across four research papers. It covers OpenAI's "Training Verifiers to Solve Math Word Problems," which introduced the GSM8K dataset and outcome-based reward models, and "Let's Verify Step by Step," which compares outcome-supervised and process-supervised reward models using the PRM800K dataset of human-labeled reasoning steps. The lecture also covers Math-Shepherd, which automates step-level annotation without human labels, and Weaver, a Stanford paper that combines ensembles of weak verifiers, including reward models and LLM judges, to close the generation-verification gap. Topics include majority voting and self-consistency baselines, credit assignment in process versus outcome supervision, reward hacking, and using trained verifiers as reward signals for reinforcement learning fine-tuning.  
  
Speaker Bio:  
Azalia Mirhoseini  
Assistant Professor of Computer Science, Stanford University  
  
Azalia Mirhoseini is a co-founder of Ricursive Intelligence, a frontier lab dedicated to recursive self-improvement through AI that designs the chips that fuel it. She is also an Assistant Professor of Computer Science at Stanford University where she directs Scaling Intelligence, a lab focused on developing scalable and self-improving AI systems and methodologies toward the goal of artificial general intelligence. Previously, she spent several years in industry AI labs, including Google Brain, Anthropic, and Google DeepMind, working on the development of Claude and Gemini. Her past work includes Mixture-of-Experts (MoE) neural architectures, now predominantly used in leading generative AI models; AlphaChip, a pioneering work on deep reinforcement learning for layout optimization used in the design of advanced chips like Google AI accelerators (TPUs) and data center CPUs; as well as pioneering research on LLM Test-Time Scaling. Her work has been recognized through the Okawa Research Grant, the Google ML and Systems Junior Faculty Award, MIT Technology Review's 35 Under 35 Award, the Best ECE Thesis Award at Rice University, publications in flagship venues such as Nature, and coverage by various media outlets, including WSJ, NYT, Forbes, MIT Technology Review, IEEE Spectrum, WIRED, and TechCrunch.

## Transcript

**0:05** · So lecture three is about verification.

**0:09** · In the last lecture when we talked about inference time scaling and the generation verification gap, basically what we discussed was that language model seems to be able to seems to know the answer to many of the hard questions, and especially with methods such as repeated sampling, or other scaling test time techniques, they can generate one.

**0:38** · But a question is, how do they.

**0:41** · How can we automatically select which answer is correct or guide the model throughout the process of answer generation.

**0:49** · So that leads us to verification where which we are learning about today.

**0:55** · So in today's lecture, we are going to learn about the following four papers.

**1:02** · And there is a progression of how the way we approach verification changed or progressed throughout the years.

**1:12** · So let's first start with training verifiers to solve math problems.

**1:18** · This is a paper from OpenAI in 2021.

**1:23** · And the motivation for this fork was that LLMs hallucinate and can confidently present wrong solutions to the users.

**1:35** · This still is true to this day.

**1:37** · Four years later, of course, the model have become significantly better.

**1:42** · There is also at the time, one of the contributions of this paper was to introduce a new reasoning benchmark around math.

**1:51** · And you can see here in blue one of these problems.

**1:55** · This is the type of problem that at the time it was hard for LLMs to solve.

**2:05** · And this led to this new dataset.

**2:08** · And that has become kind of a big part of many of the benchmarking tasks for LLMs.

**2:20** · And even to this day, this dataset is called GSM 8-K.

**2:24** · And even to this date, for smaller models and benchmarking, it's still a very useful language modeling evaluation.

**2:32** · And you can consider it for the type of evals that you want to define on your projects as well.

**2:38** · So it basically consists of 8,500 grade school math problems.

**2:45** · And the goal was for this was to have the quality and diversity of the problems.

**2:51** · But also importantly there was a focus on multi-step reasoning, meaning that to solve the problems, even though the problems were simple.

**3:00** · But the model required a few steps of reasoning to get to the answer.

**3:07** · And you could also collect the solution in natural language as opposed to pure math.

**3:18** · But the other contribution of this paper, which we are going to spend more time on, was to train a verification model where the verifier outputs the probability that a solution is correct.

**3:32** · So let's see about how this can be useful.

**3:35** · For example, the model that as humans we solve problems.

**3:40** · It would be very, very good for us to have access to a rubric or a way for us to tell whether we are correct or not.

**3:48** · And we kind of want to provide the same thing through this verifier for the language model.

**3:55** · So now how these the verifier was trained in this case is that assume that we have a question and a solution for it.

**4:04** · Then we do have a label whether is a binary label, whether it's correct or incorrect.

**4:11** · And during the training process, the generator, the language model, which is in charge of answering questions here produces PSI, which is the solution to question QI, and then we can generate-- do repeated sampling and generate multiple, in this case, 100 solutions per problem.

**4:32** · And then we create these labels based on whether they were correct or not.

**4:37** · Remember that these questions and answers were selectively designed by a lot of manual human supervision.

**4:45** · So we know what the answers-- the final answers to these problems are.

**4:49** · So we can just, based on that, create these labels for these problems.

**4:54** · And then given that we can train a verifier, because now, we have a question, we have a solution, and then we have a label for it.

**5:07** · Now, the way we use it at test time is that at test time, again, we generate a lot of answers.

**5:13** · And then we use the verifier and look at the score, basically, the log probability that is in this model now, to see which one has a higher score and use that for as our-- and show that as our final answer.

**5:31** · So in this paper, the verifier was trained not just based on the correctness prediction, but there was also a language modeling objective.

**5:41** · So the language modeling objective is also given, for example here, given these tokens corresponding to the questions, the moment we get to the solution token, we also add a loss that kind of urges-- like, motivates the model to predict or reduce the solution distance from the true labels for that solution.

**6:08** · So in this paper, they said that it helped them to have two losses.

**6:12** · One is the binary loss and the other one was the normal language modeling, next prediction token loss.

**6:20** · And the verifier itself, the architecture of the verifier is also a language model.

**6:26** · But also, this language model has a small scalar head that outputs the binary prediction on a per-token basis.

**6:38** · So basically, on a per token we are saying how close was the solution to the true labels generated by humans.

**6:50** · And then the tokens in questions are masked out because we are not optimizing for that.

**6:56** · So we generate the question.

**6:58** · We pass in, fill in the model with the questions, and we ask it to generate the solutions.

**7:03** · And we work with these two losses.

**7:07** · The way they trained the model was to fine tune the generator language model for two epochs, and then sample 100 completions per question, label it whether they were correct or not, and then train a verifier for a single epoch on this dataset.

**7:27** · So first, they did fine tune the language model on that dataset on a portion of that dataset.

**7:35** · And this step maybe it's like debatable whether we still need this step or not.

**7:41** · Because language models are already very good at instruction following and understanding math.

**7:47** · So maybe and for a lot of newer verifiers, we directly go to the training the verifier objective without any supervised fine tuning first.

**7:58** · So they did a number of ablation studies.

**8:02** · One was to create this label of correct or incorrect at the sentence level.

**8:12** · So we have a loss that only concerns at each sentence level.

**8:17** · For example, after each period looks into the previous sentence and looks whether this is a correct step given of the correct step for the solution or not, or they could do at a token level.

**8:32** · So this is very, very noisy kind of label.

**8:35** · Like basically we want every token to follow.

**8:41** · The pattern that leads to a final correct solution at the end of this generation.

**8:49** · And then the way this is used at test time is the final solution score is the score after the last token.

**8:57** · Because if you have a token label prediction per token, at the end of the day, we want only one prediction for the entire generation, whether it's correct or not.

**9:09** · And it turns out, in this case, they looked it after the last token.

**9:13** · All right.

**9:14** · So we were talking about if you have a token, a label per token, at the end of the day, we want one token, yes or no, whether this answer was correct or not.

**9:24** · And this is done in this case by just looking at the very last token.

**9:30** · And if that was a correct, then the entire answer is assumed correct, and otherwise, it's assumed incorrect.

**9:37** · So we predict for S1, S2, SM, we predict these labels.

**9:42** · And then we only look at the very last label to generate and allocate a label for the entire solution.

**9:50** · So here is-- looking back at these problems, when we get to the solution, we are looking at the token-level prediction by the train verifier.

**10:02** · And if it's green, meaning the verifier has a high score and the red ones means a lower score in this case.

**10:09** · And in this case, there were some lower scores in the middle, but towards the end, it became greener and greener, and this was a correct prediction at the end.

**10:20** · At the end, the very last stage is a green one and we assume the actual score and the verifier predictions are in this case are matching.

**10:30** · In this other case, the last verifier is red.

**10:33** · It starts off well, but it has a.

**10:36** · There is something a mistake is made, which is towards the end of this generation step and the actual score is negative and the verifier prediction is also negative.

**10:54** · So this is how basically this verifier is trained for GSM-8K And then they did some ablations or comparisons with a baseline where we just directly just fine tune on this dataset fine tune meaning with supervised fine tuning.

**11:11** · So we just take the base model and the next token prediction, or we do this verification stage where we generate 100 samples at each generation, and use the highest score of the verifier as the true as the delivered output by our system.

**11:30** · So the idea, what we can see here is that for both 6B and 175b models, this one is a GPT-3 model, I believe.

**11:44** · For both of these, verification seems to work better, especially as the training set size for the verifier increases.

**11:53** · So the verifier model eventually outperform the fine-tuning-only approach.

**12:04** · And vice versa, if you have smaller data sets-- in this case, less than 1,000 for the 175B-- the verification is not helping much.

**12:19** · \[INAUDIBLE\] Sorry, can you speak up?

**12:31** · I mean, the test summary of the 6B verification is still much higher than the \[INAUDIBLE\] on the smaller \[INAUDIBLE\].

**12:44** · The orange lines still-- Isn't it lower-- OK, I see.

**12:50** · --than 175B?

**12:52** · \[OVERLAPPING SPEECH\] OK, let me go here.

**12:56** · So this is another result which is very interesting.

**13:01** · And this is something that could potentially be a research project that you guys can look into.

**13:07** · So what they did is that they tested two approaches, one having a larger generator and smaller verifier, and two having a smaller generator and larger verifier.

**13:18** · And what they saw was that the larger generator helps.

**13:24** · The smaller verifier does better than vice versa.

**13:27** · And to some extent, this is intuitive, because if we assume generation is naturally, or on average, is a harder task than verification, then this might make sense.

**13:42** · But finding the Pareto optimal of how these two can be the sizes, with respect to each other, would be a very interesting research question, especially right now, as the base-model generators have improved a lot.

**14:00** · And also, we have access to a lot of verifiers.

**14:02** · On Hugging Face, there's a leaderboard of verification, verifier models, or reward models that can be tested against.

**14:11** · So again, this was the main message from this ablation study.

**14:19** · Another result about test-time scaling that they're showing is that, as they increase the number of completions per problem, and then they use the verifier, it seems like around 400 or so.

**14:37** · That's where they get a lot of benefit.

**14:39** · But after that, they're not getting a lot of benefit.

**14:42** · So if they sample 800 solutions and they use the verifier against that, the verifier fails to track what's best and what's not, compared to the true distribution of the solutions.

**14:57** · So one question for you is that, do you remember last time, when we talked about majority voting?

**15:05** · What was the range that we were getting out of that?

**15:08** · We showed that majority voting, although, is useful to some extent as we increase the number of samples per query, it fails, after some point, to track.

**15:20** · And that's the generation-verification gap.

**15:23** · Does any does anyone remember that?

**15:28** · OK, so that was-- we saw that the failure happens after 10 to-- we never got to 50 samples.

**15:38** · Even though the coverage goes up, the pass at one-- or basically, how we can generate, select the correct response-- fails around 50 or less for the majority voting approach.

**15:53** · But here, they're showing that, up until 400, they can increase the accuracy, and the verifier is still useful.

**16:06** · Yes, but when they have-- so they do have the true labels per problem.

**16:13** · And then, when they are testing this verifier, the verifier ranks these at each point.

**16:19** · Say, for 400, these 400 solutions, they take the highest score, and they compare that against ground truth, and that's what they're reporting here-- whether that was correct or not.

**16:31** · My question is that, in the training time, you said there's \[? over ?\] 100 \[? fusion. ?\] At test time-- and training time as well, for the verifier, but not for the generator.

**16:42** · OK.

**16:42** · For the training times, all are human \[INAUDIBLE\] but the training-- So, for each problem, the human has once generated an answer.

**16:52** · That's offline.

**16:53** · That's done once.

**16:55** · Then you take the model, generate 100 solutions per problem, and you compare each of the solutions against the ground truth, which is generated only once by humans.

**17:07** · And you see whether they match or not.

**17:09** · That's how you create the label.

**17:13** · OK.

**17:16** · OK, any questions from this paper?

**17:19** · Yes?

**17:20** · I have a question.

**17:22** · After 400, it made sense.

**17:25** · The verifier is increasing results.

**17:27** · But after that, why does it drop?

**17:29** · Intuitively, why doesn't it stay constant?

**17:33** · OK, so the question is, why does it drop after 400?

**17:37** · It shouldn't be constant, because we are not showing the coverage.

**17:41** · We are showing the output of this entire system, where the verifier ranks these, say, at this point, 800 different solutions, and we are getting the max score of the verifier.

**17:52** · But the precision of the verifier drops.

**17:56** · If two solutions are too close to each other, but one is correct and incorrect across 800, it can't distinguish between the two as well as it could do for 400.

**18:07** · So that's where we get the drop in accuracy.

**18:11** · And in reality, when they're outputting-- they created this system.

**18:15** · They said that they stopped at 100 samples because that's where they get most of the gains anyway, and that's where they're consistent.

**18:26** · \[INAUDIBLE\] it's getting longer and longer.

**18:32** · Does this mean we have more answers?

**18:34** · Repeated samples, so parallel.

**18:38** · So, same question.

**18:40** · You ask the model 100 different times to solve that.

**18:47** · Yes?

**18:48** · When they generate a label and these sort of sentences result, how do you distinguish?

**18:54** · One could just be a perfect \[INAUDIBLE\] matched one-by-one-- Because this is trained on a larger data set, and because the verifier-- and they consider both sentence-based and token-based.

**19:10** · It still works because the data that the trainer-- first of all, the verifier is a language model itself, so it knows a lot about this space itself.

**19:20** · But also, through this label training, it has been trained to be able to distinguish between correct and incorrect.

**19:31** · Yes?

**19:33** · Does it make sense to do test-time scaling on the verification itself?

**19:37** · So the question is-- let me repeat the question because one of you asked this before.

**19:42** · So the question is, does it make sense to scale the verifier, do test-time scaling on the verifier?

**19:48** · Yes, and you're going to see that in the future slides.

**19:56** · Yes?

**19:57** · The plot that you showed verification versus fine-tuning-- you showed that before, around 1,000 steps, 1,000 training size, right?

**20:06** · The fine-tuning actually does better than the verifier.

**20:10** · Does that happen again if you scale it to a higher training-- Do you mean the fine-tuning versus verification?

**20:19** · Do they cross each other-- Again, yeah, \[INAUDIBLE\].

**20:28** · If you were to actually-- if you do need that much data, for example, for a task, do you ever-- I mean, I think that you would.

**20:39** · If you have a ton of data, a whole lot of data, then fine-tuning and verification-- probably, they're going to be the same.

**20:49** · They'll converge to the same thing.

**20:52** · But the beauty of a verifier is that you are not fine-tuning your base language model.

**20:58** · You're not making it really custom to one data set or one specific task.

**21:03** · So that base model, the generator model, remains general.

**21:08** · And then, now, you have a verifier that you can lead the base model.

**21:18** · Now let's go through the second paper, another paper by OpenAI.

**21:25** · Let's verify, step by step.

**21:32** · And so this came about a couple years, less than two years, after that first paper.

**21:40** · Again, LLMs have had the same challenges.

**21:43** · They hallucinated.

**21:46** · If they're solving a problem step by step, and they make a step in a single-- a misstep early on-- it can derail the entire answer, right?

**21:56** · So the solution that they were proposing here is that they consider these two kind of approaches to reward modeling.

**22:05** · One is outcome-based reward model, and the other is process-based reward model.

**22:12** · So the outcome-based one, like we saw earlier, in the previous paper-- it generates a reward to the entire solution.

**22:20** · It's about the correctness of the solution, of the entire solution, whereas the process one assigns a different reward per step of the optimization problem.

**22:36** · And so let's take a look exactly how this training can be done for the ORM versus PRM.

**22:42** · So we have a math problem.

**22:44** · The generator-- instead of generating 100 solutions, right now, we are only looking into one solution.

**22:52** · And it has a bunch of steps-- step 1, 2, and all the way until we get to the final answer.

**22:59** · And then we have the ground truth, so we can know whether the final answer is correct or not because we can match the final answer against the ground truth.

**23:10** · Now, with ORM, we are done there because that's how we assign the label for the model.

**23:17** · But for PRM, the way they did it in this paper was that they looked into-- they had human annotators go through the steps of the generations by the model and assign a score to each step.

**23:35** · So step 1 in this case was correct.

**23:37** · Step 2 was correct.

**23:38** · And probably because, maybe, all of these steps were correct, that's why it led to the final, correct answer.

**23:46** · But basically, they created this entire data set of human-annotated, stepwise, correct or incorrect labels.

**23:58** · And the final reward for this stepwise now, again, in this case, could be-- what they propose is that can be calculated as the product of the stepwise rewards, per step of the model.

**24:13** · So they basically train the model against these stepwise annotations, and then they use that.

**24:19** · They create steps.

**24:21** · You can even ask the model to generate the answers to a solution step by step.

**24:26** · So the steps are clear.

**24:27** · They run this PRM against each of those steps.

**24:30** · They get a score.

**24:31** · They multiply them with each other.

**24:33** · They get a range of the quality of the answer.

**24:39** · And based on that, they can decide whether they output the answer or try again.

**24:47** · So this is called process supervision.

**24:50** · Obviously, there is this credit assignment, and then it's the more precise way of collecting data and assigning labels to different steps of the problem, rather than just looking at the output answer.

**25:06** · A property here that's very important-- actually, this is a really-- it could be a pitfall for test-time scaling, is that, with process supervision, we can manage the false positives way better than we can do with just outcome supervision.

**25:25** · Why?

**25:25** · Because model might hallucinate.

**25:28** · And this happens, surprisingly.

**25:29** · Model can hallucinate and get to a final, correct answer while the process for it is really wrong, whereas, with process supervision, because we are supervising, we are seeing all the steps, and we have a score for it, it's less likely that we get into the mode where the steps are wrong, but the final answer is correct.

**25:56** · Also, it encourages interpretable reasoning and human-endorsed process of solutions.

**26:04** · It's human-endorsed, again, because humans have created the labels.

**26:09** · So this paper produced this data set, PRM800K.

**26:16** · It's an open-source data set of 800k step-level labels.

**26:25** · So the way they did this was a generator model.

**26:30** · They took a language model, and they generate a large number of samples per problem in a stepwise manner.

**26:37** · And then they also did this trick of-- because they wanted to collect higher-quality stepwise labels, they took into what they call convincing wrong kind of answers, meaning that they gave higher priority to samples where the final answers were correct, but the intermediate steps were incorrect.

**27:09** · And this enabled them to be 2.6 times more data-efficient than just randomly selecting these samples and give it to humans.

**27:20** · So they did it iteratively.

**27:23** · You can have a PRM by just asking an LLM to judge a step, right?

**27:29** · You can have that.

**27:31** · So they iteratively upgraded the PRM by collecting this data and then training the PRM for it and then increasing the quality of the data.

**27:44** · And at each step, the label that was collected was either positive or negative or neutral.

**27:49** · For example, let's take a look at this problem.

**27:53** · The denominator of a fraction is 7 less than 3 times the numerator.

**28:01** · If the fraction is equivalent to 2 over 5, what is the numerator of the fraction?

**28:06** · And then there are these steps.

**28:08** · And the first step was labeled correct, second was correct, and all the way to the fifth step was correct.

**28:14** · But this last step, obviously, the model failed to do the math.

**28:18** · x should be 14, but it's 7.

**28:21** · So that was labeled incorrect, so that's how they collected the labels.

**28:29** · Here is the process.

**28:31** · So they took GPT-4 as their base model.

**28:35** · They still fine-tuned GPT-4 for both the ORM and PRM training on this data set first, so the supervised fine-tuning first.

**28:49** · And for ORM, of course, they just have the pairs of generated samples and final correctness.

**28:56** · But for PRM, they had this generator generate the sample and then the stepwise correctness label.

**29:04** · For ORM, the final score was the score of the final token in the completion.

**29:09** · Again, they again went to the token-level approach for ORM, but for PRM, it was the product of probabilities for every step.

**29:21** · Now let's take a look at some of the solutions.

**29:24** · They were showing that PRM outperforms ORM and majority voting.

**29:29** · So again, here, n is the number of solutions per problem.

**29:33** · Majority voting, again, fails after, in this case, 100 or so samples.

**29:39** · The blue line is the ORM model, and the orange one is the PRM approach that is doing better.

**29:49** · But they noticed that PRM detects correct solutions for some of the very rare occurrences of a correct answer, some problems with less than 5% correct answers in the distribution of samples.

**30:06** · They also showed the benefit of larger data in and this active learning approach that they had, again.

**30:16** · And the other observation that they were showing is that PRM seems to be more data-efficient.

**30:25** · So the number of labels that they collected for PRM-- if they match that against ORM, both PRM and ORM benefit from more and more labels, but it turns out that the PRM is more sample-efficient, right?

**30:43** · So if they have 100 solutions labeled per problem for an ORM model, that's like having one solution per problem, based on the PRM approach and so on.

**31:01** · The other interesting property-- and that's what we all should strive as we are training these kind of verifier and reward model, is the generalizability to new domains and new data sets.

**31:16** · Here, what they're showing is that majority voting actually is better than ORM in terms of how it generalizes, but PRM is better than majority voting overall, and it can tolerate a whole lot more distribution shift than majority voting.

**31:37** · And so, overall, this seems like a much better approach here.

**31:43** · Any questions?

**31:46** · Yes?

**31:47** · So PRMs obviously could lead to false credit assignment if a step looks good but doesn't actually contribute to the final answer.

**31:55** · Are there domains that you would expect PRMs to actually hurt?

**32:00** · So the question is, can PRM hurt sometimes because the final answer might still be incorrect?

**32:08** · So the truth is, a lot of the newer approaches combine the two.

**32:13** · The reality is they combine both the PRM- and ORM-based solutions because you want to get the benefit of both approaches.

**32:22** · And the other thing is that the threshold that you can define for PRM, then, is also a hyperparameter that now you have introduced that you have to deal with and optimize for your system, and that's an additional complexity here.

**32:38** · But yes.

**32:40** · For the previous one, the plot, does it make sense to do this comparison?

**32:46** · Because PRM requests much more labels than ORM.

**32:50** · So do they show a plot where the x-axis is \[INAUDIBLE\]?

**32:54** · Yeah, I think we were trying to.

**32:57** · Yeah, because they also mentioned that it's hard to compare.

**33:00** · And they did manage to have-- because it's true ORM needs k labels for problems, but PRM needs k times some number of steps.

**33:14** · But then it's very hard to control that number of steps of-- how do you exactly control?

**33:18** · But they did try to manage that, and I believe some of the graphs-- they do that.

**33:23** · But that's a good point.

**33:25** · Yes?

**33:25** · What does "majority voting" mean in this context?

**33:29** · So "majority voting" is you have n samples.

**33:33** · You don't have any access to any reward model.

**33:38** · You just see which sample or solution is repeated most, and you take that as your final answer.

**33:44** · \[INAUDIBLE\] the reasoning process, so are you also going to match on the reasoning process?

**33:49** · No, you look into the final answer in this case.

**33:54** · In this case, are they using the same PRM at 100k for all of those tasks?

**33:59** · Or are they using different terms for each \[INAUDIBLE\]?

**34:03** · Because they're talking about generalization, I assume this should be-- The same?

**34:08** · The same one.

**34:08** · But yeah.

**34:14** · Yes?

**34:16** · How does this avoid when the reasoning is actually bad, but graded high?

**34:20** · For example, if you go back to slide 23-- This one?

**34:26** · \[INAUDIBLE\] Yeah, this one.

**34:31** · What if the reasoning is, let's call the numerator x, and then x equals to 14, and \[INAUDIBLE\].

**34:41** · How does that avoid \[INAUDIBLE\]?

**34:44** · So you were saying the PRM can give a high score?

**34:48** · What if it's skip all the reasoning?

**34:51** · Let's call the numerator x, and then x equals to 14.

**34:54** · How does that avoid that kind of hacking?

**34:57** · Sorry, I don't get it.

**34:59** · Can you speak up?

**35:00** · What's the alternative scenario you are talking?

**35:04** · The reasoning step would just be numerator x, and then x equals to 14.

**35:10** · And how does the PRM avoid that kind of real \[? typing ?\] scenario?

**35:14** · I think the model directly skips some steps and directly generates the answer, like, \[? speeds ?\] some of the processes.

**35:23** · So these programs are trained like-- programs can also see the previous steps, like the question's previous step.

**35:30** · Here is the current step.

**35:32** · Score it.

**35:33** · Right?

**35:35** · So if x is 14, then it's great, right?

**35:37** · So it doesn't really encourage the thinking process of going to step-by-step.

**35:43** · It doesn't, no.

**35:44** · No, it doesn't.

**35:45** · But you can prompt the model to do this because you're not changing the model.

**35:50** · You're not changing your generator.

**35:54** · That failure mode could be when you were fine-tune your generator model.

**35:58** · Then the model stops reasoning and just generates a final answer that the PRM likes, right?

**36:04** · But you're not touching your generator.

**36:07** · The generators can still be prompted to do reasoning, create these steps, and then the verifier just scores them.

**36:16** · Let's say we want to use the PRM to train the-- Yeah, then you have to be careful.

**36:22** · Then you have to make sure that the chain of thought makes sense.

**36:26** · And again, the way you train your PRM can also be aware of that because your PRM could be-- these are human-generated labels in this case, right?

**36:41** · If we had skipped all of this, and then we would go to x 14, probably, the human says, this doesn't make sense.

**36:49** · This step is lower, because this step is skipping a few reasoning steps.

**36:56** · Does that make sense?

**36:57** · So these labels are created by humans here.

**37:00** · \[INAUDIBLE\] So if the labels are not generated by humans-- and we are going to see that in the next paper-- yes, that is definitely a caveat and something that you can make sure.

**37:14** · But there are ways to handle that as well.

**37:16** · So for now, let's assume these are human labels, so the processes are labeled in a way that they make sense as well.

**37:23** · We have so many things to encourage these generation to make sense.

**37:28** · First of all, the generator should generate the steps.

**37:33** · The PRM is trained on human annotations that they also make sure that this step makes sense, given the prior steps.

**37:43** · Any other questions?

**37:48** · OK, let's go through the next paper, Math-Shepherd.

**37:53** · Verify and reinforce LLMs step-by-step without human annotations.

**37:57** · So we're getting to, what if we didn't want to collect that many annotations from humans?

**38:06** · So again, motivation is that having stronger verifiers shows the potential to really improve model's reasoning behavior, especially if you do test-time scaling.

**38:22** · PRMs have shown more potential than ORMs, but they require a lot of data, and it's hard to collect these data.

**38:30** · So can we automate the process of label collection for PRMs?

**38:37** · So this paper talks about two kind of approaches.

**38:41** · One is automatic annotation, and also brings the reward model into the loop of generator optimization via a reinforcement learning approach, which-- we are going to briefly mention that.

**39:00** · So, in this case, the way they try to go about this automatic annotation of steps was that they define the quality of the reasons step as the potential of this step to reach to the final, correct answer.

**39:21** · So let's say we are at a given step.

**39:24** · We sample N completions from that given step and see the potential for a correct solution at the very end.

**39:34** · And they introduce two ways of doing this.

**39:37** · One is the hard estimate, where a step is annotated as a success if any of those n generations after that step gets to a final, correct answer.

**39:55** · The soft estimate measures the frequency, like what portion of the generations after a current step reached the final, correct answer?

**40:04** · So here is how it works.

**40:07** · Say here is the problem, and this is our current state.

**40:11** · Instead of just sampling one step, N is 3 in this case, so we sample three steps.

**40:18** · And then we continue, and we measure the frequency.

**40:23** · In the soft estimate, we measure the frequency of correct answer at the very end.

**40:28** · In hard estimate, we see whether any of these are correct or not.

**40:34** · So hard estimate would be 1 for step 1.

**40:37** · Soft estimate would be 2/3 for step 1.

**40:43** · Anyone can name a challenge or a drawback of this approach?

**40:53** · So basically, this soft or hard estimation is replacing the human annotations.

**41:03** · So we're getting a score per step by just rolling out more samples from that step and seeing whether we reach to the final, correct answer or not, and assume that we do have final labels for these problems.

**41:21** · Yes?

**41:22** · So we-- for unpredictable paths \[INAUDIBLE\] lower when the unpredictable path could be built \[INAUDIBLE\].

**41:35** · Sorry, speak up again.

**41:36** · If it's unpredictable-- Or unusual approaches to solving a problem.

**41:42** · It could be scored as low or something, while that might be the way to be able to solve that problem.

**41:48** · It might be a really hard problem.

**41:50** · Now likely to lose that path to that solution.

**41:54** · That is correct.

**41:55** · So basically, say N is 3 here.

**41:58** · Maybe we needed N equal 100 to see that final, correct trajectory to score this step, but we won't see that if we just look into 3, and then we give a score of 0.

**42:15** · Anything else?

**42:23** · Yes?

**42:24** · I guess this is similar, but if you're dealing with a hard question, if you're taking the approach of generating a lot of samples, a lot of the samples can just not be correct or not be the correct way to do it.

**42:34** · So-- You don't get any signal for hard problems in this case.

**42:42** · That's right.

**42:44** · \[INAUDIBLE\] Exactly.

**42:49** · I think this is probably-- these two that you all mentioned here-- for hard problems, you don't get signal.

**42:56** · The other one is, what if there are wrong steps in the middle, and we got to the final, correct solution?

**43:03** · We still label those steps as correct.

**43:08** · So the hope is that, if you have more samples, it shows the wrongness in one of these trajectories, but it's not guaranteed.

**43:24** · So here's the verification process.

**43:27** · You sample N again, sample N candidate solutions, score them using the PRM, and you select the highest PRM score across the generated samples.

**43:42** · They also took this PRM and trained the model with this PRM to encourage the model to generate steps that are scored higher and higher by PRM.

**43:53** · So PRM basically served as the reward model for this.

**43:58** · So they looked into the hard versus soft annotations, and although the loss function as they increased N would be-- it seemed like the soft annotations were doing better.

**44:14** · But somehow what they observed with the N equal 4, the depth of the trajectory completions to collect these labels-- that's where they get their best results anyway.

**44:31** · So it really didn't matter whether they used the hard estimate or soft estimate, and they went with the hard estimate at the very end because it was just easier to measure that.

**44:42** · So here is another comparison with baseline.

**44:51** · "SC" is self-consistency.

**44:53** · It's another name for majority voting.

**44:56** · Which solution was most consistent?

**44:59** · That's the red one.

**45:01** · ORM is the blue one, and the SHEPHERD is this PRM approach, is the green one.

**45:07** · And the interesting part here was that there was no human annotation.

**45:12** · All the annotations were modeled, generated, or the mechanism that they introduced.

**45:21** · Here, they also compare with PRM800K, which was the verifier in the previous paper that was trained.

**45:30** · And it outperformed that as well on MATH, which is like a much harder set of-- this data set is more difficult than GSM8K, and they were getting an even higher delta in there.

**45:46** · They also compared these results with different types of verifiers again across GSM8K and MATH500 problems.

**45:59** · And you can see that the difference between these models and these approaches-- and there is a notable difference between these models and the baselines, which is self-consistency approaches.

**46:18** · And this is true across different models-- LLaMA-70B, LLema-34B, and DeepSeek-67B.

**46:29** · They also showed that they can get even better.

**46:31** · They can make the model even better if they RL the model against the PRMs that they trained.

**46:37** · So, in this case, the Math-Shepherd, on their approach-- basically, taking Mistral-7B, this model, and then they PPO it against this PRM.

**46:50** · They're getting much higher results, compared to doing this RL with just an ORM.

**46:59** · The delta here is slightly less, I would say, than just the test-time scaling, but this is also another way for the models to self-improve.

**47:09** · You generate the annotation by the model itself.

**47:14** · You train the PRM and then use that PRM to improve the generator model as well, both at test time and with this RL fine-tuning.

**47:22** · So it's multiple levels of using the model itself to generate data and RL reward-signal for itself.

**47:38** · And then they can do RL and PPO and do verification on top, and they get even better results, but it seems their optimizations are plateauing at some point.

**47:51** · Any questions from this paper?

**47:56** · Yes?

**47:56** · Are there ways to build PRMs that incentivize self-error correction, which I imagine would be a desirable thing?

**48:03** · But if we're only rewarding each step being correct, we don't necessarily end up reinforcing-- you get a lot of incorrect steps back and stuff like that?

**48:13** · So encourage PRMs to do more self-correction?

**48:18** · Yeah.

**48:19** · Yes, absolutely.

**48:20** · For example, one of the methods that can be done is that you have a rubric, or a set of rules, that you give the model as your scoring step.

**48:32** · So the model can check the step against this rubric that you have designed for this data set, and that can be used as extra signal whether this step makes sense or not.

**48:45** · For example, use a calculator in that case, in the equation that we are seeing.

**48:51** · If the model could do tool use or use a calculator in that case, it could solve that problem easily-- could, for example, use SymPy.

**49:02** · So there are ways to bring more supervision and more signal and enable the model to use tools and test-time scaling and agentic approaches to improve the verification process.

**49:19** · Yes?

**49:20** · \[INAUDIBLE\] verifiers, do they control the amount of test-time compute?

**49:29** · I believe so.

**49:31** · You mean "test time" as when they're using the verifier, like a baseline verifier, versus themselves?

**49:37** · I'm actually not sure if they do that when they're doing process versus ORM, because, again, that's really hard to do.

**49:46** · \[INAUDIBLE\] because you're scaling things at different rates.

**49:52** · Yeah, I think that could actually be a question that you could investigate.

**49:56** · You can sample more in the generator.

**49:58** · You could sample more in the verifier.

**50:01** · If you're controlling for a fixed compute, how do you allocate that?

**50:07** · So one of the challenges here is that, usually, the ORM and PRM should come from the same data for us to do a good apples-to-apples comparison, because if you do train a PRM, and someone else train an ORM, it makes things a bit harder.

**50:21** · The training data also matters a lot.

**50:26** · Any other questions?

**50:27** · Yes?

**50:29** · Do you could back to the previous slide?

**50:31** · Yeah, I was just-- oh, no.

**50:33** · Basically, for this one, I was just curious as to why, after using RL, they stuck with evaluating performances with greedy decoding.

**50:41** · I was just curious whether or not raising the temperature would have made a difference, or that was the only way they could have seen the smallest delta.

**50:55** · So the question is why they stopped greedy decoding, why they didn't do temperature changes and test-time scaling again, right?

**51:01** · I think that's what this slide is.

**51:04** · So then, in this case, the verification is done against 256 outputs.

**51:12** · So the previous one is no verification, right?

**51:16** · The verifier is just using the RL training here, just at test time as well.

**51:25** · I think it's something that they didn't do, and it would be interesting to see.

**51:28** · What if they repeat the process again, generate another set of labels, and train a verifier, but starting from this RL-PPO'd model?

**51:47** · OK, let's get to the last paper, shrinking the generation-verification gap with weak verifiers.

**51:55** · So this is a paper from Stanford that came out a couple months ago at this point.

**52:07** · So it's a NeurIPS 2025 paper.

**52:11** · So the motivation, again, is the same.

**52:18** · We still have a generation-verification gap, but the approach here was a bit different.

**52:25** · Here, we were not training a new verifier.

**52:27** · We were thinking, can we reduce the generation-verification gap by using inference compute and inference scaling, and specifically by using an ensemble of verifiers?

**52:39** · Because when we say "weak," we just assume that no verifier is perfect.

**52:44** · So that's the weakness.

**52:45** · We didn't purposefully choose bad verifiers.

**52:48** · These are the best verifiers that are out there.

**52:50** · But we are using an ensemble of them to create a single, much more capable verifier.

**53:02** · So the property of these verifiers is that they do correlate with the true label of the solution, but they have imperfections.

**53:12** · And there are two types of these verifiers.

**53:14** · We learned about PRMs and ORMs, but another one that we briefly discussed a few minutes ago is that we can use LLMs themselves as a judge.

**53:25** · We can show it an answer and ask it, do you think this is correct or not?

**53:31** · The prompt could be literally that.

**53:33** · Or we can have the model use tools and use rubrics and all that to generate a score for a model.

**53:39** · So that's a whole category of verifiers that we can use on top of just PRMs and ORMs.

**53:46** · So here, this first graph just shows how ensembling and using a number of verifiers that are-- they could be trained by different labs on different data sets.

**53:59** · And there are all these language models that take a query as input and give it a score on the output side.

**54:05** · Here, we are seeing these four data sets.

**54:09** · So in this case, we are showing the performance of top 1, versus top 5, versus top 10 verifiers, based on how good they are in some ranking system.

**54:21** · Overall, it seems like just ensembling them with each other and using them at test time does improve things, but not necessarily in a monotonic way.

**54:41** · But the thing that always helped was that, if we train a model, a way for them to add them together-- so assign weights for different members of the ensemble, if we have labels from them.

**54:56** · Here, we have two methods, Naive Bayes or logistic regression.

**55:00** · These are very simple methods.

**55:02** · Basically, you add a single weight per verifier to score them together.

**55:07** · And if you have a training set with labels, you can basically come up with these weights, and now these results are on the test set, corresponding to those tasks.

**55:20** · So you basically say, for MATH500, I have a set of labels.

**55:25** · I use that to average my verifiers, find the weights, and then I use these averages on test data.

**55:33** · So it seems like it does give a lot of improvement, just this simple task.

**55:41** · Now, you can do other things.

**55:43** · So the way Weaver works is by this "score, weight, and select" approach.

**55:48** · So, in the first step, we are going to score outputs of the verifiers and normalize them so they're all on the same scale, and filter out the low-quality verifiers.

**56:03** · So in this setup, even, we are assuming we have access to very limited labels that we can say, OK, these verifiers are just so bad against our labels.

**56:11** · We just remove them from our ensemble.

**56:14** · We have noticed that this is a very important step.

**56:17** · Your verifiers should be above a certain quality to even be let in the pool of verifiers.

**56:24** · So then you have your verifiers.

**56:26** · You have your LLM judges.

**56:27** · You have your reward models.

**56:29** · And then you get these scores from them, whether it's 0 or 1 or the log prob of correctness per verifier.

**56:38** · And then what Weaver did was to use weak supervision to estimate the verifier accuracy with very small data, labeled "data."

**56:51** · And then we use those weights to combine the verifiers' output and assign a score.

**56:58** · I go briefly through how this weak to strong supervision works.

**57:02** · Some of you, if you have taken deep-learning courses, or even CS229S last time, we talked about it, about weak to strong supervision.

**57:13** · There's a whole body of work here.

**57:15** · Weaver was specifically motivated by the work by Snorkel, by Alex Ratner et al., and other work from Stanford.

**57:28** · So here is how we have these weak verifiers, like weak signal from our verifiers, and combine them together to get a stronger signal.

**57:36** · The setup is the following.

**57:38** · We have n queries.

**57:40** · For each query, we create k solutions.

**57:43** · And then let's assume we have m verifiers.

**57:46** · So we have a total of n times k times m labels.

**57:51** · And our goal here is to get this probability of query i, sample j equal to 1, given all the labels that we get from all the verifiers.

**58:05** · So how do we estimate this probability correctly?

**58:10** · The assumption in Weaver is that each verifier captures independent aspect of the correctness.

**58:17** · So this is a key assumption that we made.

**58:20** · To some extent, the reason we get-- so think about it this way.

**58:24** · If you have a pool of verifiers, if all of them agree on the score that they give to any sample, then we are not learning anything new from them, if all of them are 100% or the same score.

**58:36** · The signal here is on similarity and dissimilarity across this whole set of verifiers with each other.

**58:45** · So, under this assumption, we can write this probability for the response being correct, given the labels that we have, and then we use two sets of equations.

**58:56** · Again, this the first equation is-- we can write it this way because we assume every two verifier i and j are independent from each other.

**59:06** · The second equation is just the Bayes-- the way probability works.

**59:13** · There's no assumption in writing this.

**59:15** · And given these two, we can write an optimization and come up with the weights that we can assign to each of the verifiers.

**59:29** · And here, we are comparing the results with a naive ensemble approach, and it turns out that it does help.

**59:37** · In some cases, the gains are more significant-- in GPQA Diamond and MATH and MLU Pro.

**59:45** · And each of these problems that are relatively hard problems-- for example, the GPQA, our baseline, is already low, but the verifier-- this way of weak to strong aggregation of responses is helping getting a large boost, over naive ensembling of them.

**1:00:07** · Now, there are different ways that we can scale the verification compute.

**1:00:11** · We can sample more generations.

**1:00:13** · So, instead of 10 samples, we can do 100 or 1,000.

**1:00:17** · We can use larger models for generation and verification.

**1:00:21** · We can increase the number of verifiers in the pool.

**1:00:27** · And in general, there are different ways to assign flops or scale inference compute for solving a problem.

**1:00:37** · Here, we are comparing some of these methods with each other.

**1:00:41** · So the dashed, dark red line is the Pass@K Oracle, meaning that if we had an Oracle selector, that would give us the correct answer.

**1:00:57** · We don't have that, and that's why we are training these verifiers.

**1:01:01** · The purple one is Weaver Supervised, and that's assumed that we have a large body of labeled data and we can use them to learn these weights.

**1:01:10** · The blue one is the Unsupervised.

**1:01:12** · In this case, we're using 1% of the training labels for each data set.

**1:01:18** · The orange one is the Naive Ensemble, meaning we just average them, average the verifiers without any special treatment.

**1:01:28** · We still are filtering and keeping the good verifiers in the loop.

**1:01:33** · And then all of these are significantly better than methods such as Majority Voting or Multi-Agent Verification.

**1:01:41** · And Multi-Agent Verification, or MAV-- it's just based on prompting LLMs and asking them to score a given response, based on different kind of aspects that is produced, so a rubric-based, which doesn't do that much better-- or actually worse, in these two cases-- than Majority Voting.

**1:02:09** · But something to notice here is the drastic gains that the model can have, going from something like slightly over 40% to over 70% on these hard problems and, in this case, matching a model like o3-mini.

**1:02:29** · So the thing that is interesting here is that we can use this weak to strong supervision to reduce the gap between model classes.

**1:02:41** · So what we are seeing here is that, if we take a generator model of Llama 3.1 8B Instruct, and the verifier model which is the pool of verifiers that are 8B and below, we get an average of 70% on these data set.

**1:02:59** · And this is almost comparable to the accuracy that we get with majority voting, but when our models are at 70B.

**1:03:10** · So we are making the model, making this 8B model, roughly the same as the 70B class by just doing this inference scaling and using the verifier.

**1:03:27** · And in this case, unlike what we saw in most of the previous lecture, we are talking about the end results.

**1:03:33** · We're not talking about the coverage.

**1:03:35** · We're talking about the solution accuracy of the entire system.

**1:03:41** · And here again, in this case, for when we do the same, apply the same generation and verification to 70B class of models, we are getting an average accuracy of 86.2% on these data sets.

**1:03:55** · And this is very comparable to o3-mini, which has a much-- which is like a proprietary model and in general, is a different class of models.

**1:04:10** · So this shows how much verification, or this work and verification, can help with the results.

**1:04:16** · Another work that was done on increasing the usefulness of something like Weaver is that a challenge with ensembling verifiers is that you have a ton of models that now you need to run for each solution to get a score, and then to average them.

**1:04:34** · And that increases the cost, especially if, instead of one sample per query, you have 100 samples, and then you want to create all these scores.

**1:04:43** · So instead, the proposal here is that, what if we do train Weaver once and then distill it into a much smaller model?

**1:04:53** · And that's how, instead of running each of these LLM judges or reward models per sample, we just take this distilled LLM, which-- in this case, we showed that it could be really, really tiny, like something like 400 million parameters, as opposed to the original model, which was in the 70B range.

**1:05:15** · And it turns out that, with this distilled model, we can capture 97% of accuracy of this large pool of verifiers, but significantly-- in this case, 99%-plus-- use less compute at test time.

**1:05:33** · And these distilled version, and the original version-- they're all open-sourced, and the checkpoints are available, if any of you are interested in working with them in your agentic or test-time scaling projects.

**1:05:54** · And here is another graph.

**1:05:55** · Here is the distilled one, which is the light blue one, and the original Weaver is the dark blue one.

**1:06:02** · And we are comparing, again, the efficiency, the success rate over the inference compute, the total inference compute that we are spending on this data set.

**1:06:14** · And the distilled one, obviously, is significantly more efficient.

**1:06:20** · But even the original Weaver-- because it reaches higher levels of accuracy at those levels, it becomes more flop-efficient than models like naive ensemble and majority voting.

**1:06:35** · And let's do a quick recap.

**1:06:39** · So today we covered four papers that also show the trajectory of how this work, research on verification has progressed over the last four years.

**1:06:53** · We talked about how verification can improve training, can improve the outcome and the quality of results, both during training and inference.

**1:07:07** · Process reward seems to be very useful and, overall, very effective, and more so than the outcome rewards, but perhaps we need to combine them to get the best results, both PRMs and ORMs.

**1:07:23** · And we also, in \[INAUDIBLE\], learned that scaling-- you need a lot of data.

**1:07:28** · And the more data you throw in the verifier training, it becomes better, and you can use it during your RL fine-tuning to increase the quality of your generator as well.

**1:07:40** · And the Weaver work took a whole different approach to verification, and that was just doing this weak supervised optimization on an ensemble of verifiers.

**1:07:52** · And in a way, we are using test-time scaling, but by bringing more verifiers, rather than sampling a single verifier more to get the results.

**1:08:02** · And it turns out we can distill that and capture a whole lot of the quality from a much smaller model.

**1:08:09** · And with that, I can conclude the class.

**1:08:13** · Any questions?

**1:08:15** · Yes?

**1:08:15** · \[? Are ?\] all the papers were on \[INAUDIBLE\] reasoning benchmarks.

**1:08:21** · Do you think there's anything else that could work for our project, other ways to evaluate the models?

**1:08:28** · Like coding?

**1:08:29** · Other ways to evaluate the model-- you mean other areas, like coding, would be a very interesting area for reasoning.

**1:08:38** · So there were some coding problems in some of the benchmarks here, so it's not just math.

**1:08:45** · But coding is also a very interesting area for verification.

**1:08:52** · We will talk about code monkeys.

**1:08:55** · This is a paper that-- instead of directly training a verifier, you can make the model create a test-time system to make the model generate unit tests, and those unit tests become your verifier.

**1:09:08** · So that's an entirely different approach.

**1:09:11** · But these kind of verifications should also be useful for any kind of reasoning task.

**1:09:22** · Yes?

**1:09:24** · I'm curious, how do generation-verification \[INAUDIBLE\] using models that internalize this \[INAUDIBLE\]?

**1:09:37** · OK, so the question is, for reasoning model, how does the generation-verification, or this kind of test-time scalings work for them?

**1:09:45** · It actually helps them as well, still.

**1:09:48** · But the reasoning model-- we're going to talk about them in this class.

**1:09:53** · But basically, what they're doing-- a big part of it is to generate these reasoning steps, use the reward for it, and do an RL loop, and generate positive trajectories, and then use that positive trajectories as part of training for the next round.

**1:10:09** · So the test-time scaling is inherently used to generate data and generate the training process.

**1:10:17** · But they still would benefit because they still could explore different parts of the solution space with more sampling.

**1:10:27** · \[INAUDIBLE\] existing knowledge, using \[INAUDIBLE\].

**1:10:34** · Do you think, in the future, these two paradigms will converge, or do you think maybe repeated sampling will only be used for generating training data for \[INAUDIBLE\]?

**1:10:48** · So the question is, would we converge to a future where these kind of test-time scaling, repeated sampling \[INAUDIBLE\] just for training time to create the data, and then, at test time, we just ask the model once?

**1:11:01** · I think that's the direction we want to go.

**1:11:03** · We want the model to be really, really good at pass at one.

**1:11:07** · The first time we ask it to do something, we want it to generate, and that increases the efficiency and all that.

**1:11:13** · That would be the hope.

**1:11:14** · One challenge, though, with making the model-- to make the log probs of the model-- to sharpen through one answer is that the creativity and diversity of solutions may be lost somehow during the training.

**1:11:30** · So surprisingly, we still like models have a lot of creativity and diversity in the way that they think.

**1:11:41** · And that's a good feature that we want to have in the models.

**1:11:46** · Yes?

**1:11:48** · Does it matter if generator and verifiers have very different architectures-- for example, if the verifier is a mini version of the generator, versus if they're very different architectures?

**1:11:59** · Does it matter-- Which one is empirically better?

**1:12:04** · OK, so the question is if the generator and verifier is from the same family or not.

**1:12:10** · That's a good research question.

**1:12:13** · I think, in general, it's interesting.

**1:12:16** · Models like their own generations and their own way of interpreting results much better than using a different family of models.

**1:12:26** · We are going to talk about a paper that talks about how certain models can benefit from, like a different class of verifiers over themselves.

**1:12:37** · But specifically, I am unaware of a study that has looked into that specific question of same size and family, versus different size, different family-- how that changes the behavior of the model.
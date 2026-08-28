---
title: "Stanford CS329A Self-Improving AI Agents | Part 8 | Agentic Evaluations and Long Horizon Tasks"
source: "https://www.youtube.com/watch?v=8JAqLnTaZu4&list=PLangBM27OtEA&index=8"
author:
  - "[[Stanford Online]]"
published: 2026-08-03
created: 2026-08-26
description: "Want to dive deeper? This curriculum is covered in the following online courses:- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html- XCS329 graduate course:"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=8JAqLnTaZu4)

Want to dive deeper? This curriculum is covered in the following online courses:  
\- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html  
\- XCS329 graduate course: https://online.stanford.edu/courses/cs329a-self-improving-ai-agents  
  
A similar curriculum is covered in XCS329z https://online.stanford.edu/courses/cs329z-engineering-ai-agents  
  
Follow along with the course schedule and syllabus: https://cs329a.stanford.edu/  
  
View the course playlist: https://www.youtube.com/playlist?list=PLangBM27OtEA  
  
Video Summary:  
This lecture video from Stanford's CS329A, Self-Improving AI Agents, taught by Aakanksha Chowdhery on November 17, 2025, covers methods for evaluating AI agents on long-horizon and economically valuable tasks. It reviews METR's time-horizon methodology, which measures the task duration models complete at 50 and 80 percent reliability across the HCAST, SWE-bench, and RE-Bench suites, showing that model capability has roughly doubled every seven months, from seconds for GPT-2 in 2019 to nearly an hour for Claude 3.7 Sonnet in 2025. It also covers GDPval, OpenAI's benchmark that scores model output against work from industry professionals across 44 occupations and nine sectors, where win rates rose from 12.4 percent for GPT-4o to 47.6 percent for Claude Opus 4.1. Stanford's Deep Scholar Bench, also discussed, tests whether models can generate literature review sections for academic papers by scoring knowledge synthesis, retrieval quality, and citation verifiability. The lecture closes by detailing recurring agent failure modes, including poor planning, incorrect tool selection, premature task abandonment, and repetitive action loops.  
  
Speaker Bio:  
Aakanksha Chowdhery  
Adjunct Professor of Computer Science, Stanford University  
  
Dr. Aakanksha Chowdhery is pushing the frontier of agentic LLMs, focusing on recursive self-improvement and long-horizon agents that learn and deploy in the real world. She is one of the few researchers globally who has led frontier model training end-to-end, across both dense and mixture-of-experts (MoE) architectures. At Google, she led the 540B PaLM model, the largest densely trained language model in the world at the time. She subsequently drove pre-training and scaling of Gemini's MoE models across multiple generations, and contributed key components to PaLM-E, Med-PaLM, and the Pathways infrastructure underpinning Google's large-model efforts. She went on to build and lead pretraining teams for open intelligence efforts at Reflection and Meta. Earlier, she held research roles at Microsoft Research and Princeton. At Stanford, where she earned her PhD, she teaches CS329A (Self-Improving AI Agents) and serves as Program Chair for MLSys 2026.

## Transcript

**0:05** · Today's lecture will focus on genetic evaluations and long horizon tasks.

**0:10** · How many of you have had to run an evaluation for your project to do whatever you've been doing?

**0:21** · No one is running an evaluation.

**0:22** · How are you guys doing any projects?

**0:26** · What evaluation tasks have you used for agentic evaluations?

**0:33** · I'm going to call people out if I don't get answers.

**0:38** · What have you been using in your project?

**0:42** · I wonder for agentic evaluation, do you mean like it has to be something like a \[INAUDIBLE\] bench or knowledge task or body of knowledge task?

**0:50** · All of those count.

**0:51** · OK.

**0:51** · Yeah, so then, I guess, like \[INAUDIBLE\].

**0:55** · OK, so that's a multi-hop question answering task.

**0:58** · So \[INAUDIBLE\] bench would also count.

**1:01** · What else have you folks been using?

**1:07** · There's no other answers.

**1:09** · What about you?

**1:11** · Yeah.

**1:16** · I'm working on a private Wiki for my employer.

**1:18** · And I sat down and make notes out of that and then feed that into a coding agent.

**1:23** · OK, nice.

**1:25** · It's a private Wiki question/answers.

**1:27** · So I think a lot of this lecture will focus on what is challenging about agentic evaluations relative to where things have been before and how things become harder.

**1:38** · The papers that we'll cover to cover this topic will be focused on measuring the ability of these models to complete long tasks in terms of, what's the length of the task?

**1:49** · Length, as in time horizon of the task that the models can complete.

**1:54** · Also second paper that we'll look at is GDPVal which was a recent benchmark that was released by OpenAI.

**2:01** · This will focus on how the models perform on real-world, economically valuable tasks.

**2:05** · So there has been a lot of discussion around the models can do tasks that real-world professionals can do.

**2:12** · So this is measuring that in a very real sense.

**2:15** · And then the last task will very much focus on deep research style tasks.

**2:19** · So it is called DeepScholar-Bench.

**2:20** · It's out of Stanford.

**2:22** · And it's a live benchmark that focus on generative research synthesis.

**2:25** · So it takes a bunch of papers and then tries to write the related work section, a task that I have always wanted the language models to go do for the papers that I write.

**2:35** · So this actually measures how good of a job does the model do in solving these kind of tasks?

**2:44** · So one of the challenges of measuring intelligence or progress of AI is that we have to measure what matters.

**2:54** · How are the models progressing?

**2:55** · So when we started about four or five years ago, even the fact that the models could generate any explanations was such a big deal.

**3:03** · And now we measure the progress of AI in terms of whether we can forecast how it will influence economics or how it will influence safety.

**3:13** · Traditional benchmarks, which involve chatbots or which involve, say, question/answering or single shot just answering something that was already in the context are starting to saturate it fairly quickly.

**3:26** · However, we do need to measure, both in terms of capability and economic impact, how these models are progressing so that we can see what their impact will be in the coming years.

**3:38** · So in terms of measuring capability, what we covered today is we are looking at the task, of how long or how complex of a task can these models accomplish?

**3:50** · And the second question we ask is, what is the economic value of the task that these models can do?

**3:56** · Or can they do real-world tasks that humans can currently do?

**4:00** · And the two papers that we are referencing here is-- or the two metrics that we are referencing here is that METR refers to the time horizon metric calibrated by human professionals.

**4:12** · And GDPVal compares the win rate of model performing a task relative to experts.

**4:19** · So both of them are equally valid metrics in certain ways.

**4:23** · And the insights are very similar.

**4:24** · But the trends that they measure in terms of how models perform are quite different.

**4:32** · So let's start with the first one.

**4:35** · So, when you're talking to a chatbot, if you were talking to a chatbot, say three, four, or five years ago, usually after a first couple of rounds in multi-turn conversation, the model will be lost.

**4:48** · It doesn't keep context of what you were talking to it about.

**4:52** · Today as you talk to these models, the conversation can go pretty long.

**4:56** · So it does keep that context.

**4:58** · And that relates then to the question of, what is the duration of the task that the model can complete.

**5:04** · So that's just the duration question.

**5:06** · And then the second question is, what's the percentage success?

**5:09** · Can it do so reliably?

**5:11** · So METR, this particular benchmark focuses on duration of the task that model can complete.

**5:18** · And then it associates a reliability metric of like, will it complete it with 50% success or will it complete it with 80% success?

**5:26** · And so on.

**5:29** · And the universal anchor for these tasks ends up being the, how much time will it take humans to complete if they were professionals in solving these tasks?

**5:42** · So there are three task suites that are used to design this particular benchmark.

**5:48** · One is extremely small.

**5:50** · So one to 30 seconds.

**5:51** · It basically focusing on just atomic actions.

**5:53** · So in software engineering, can you open a file?

**5:56** · Can you do something small?

**5:58** · The second one is HCAST, which focuses on more 1 minute to 30 hours style of tasks, which is basically talking about different software and research engineering tasks.

**6:09** · And then finally, RE-Bench that's actually giving a full ML research style tasks, which can go on as long as eight hours.

**6:17** · So you've seen like AI scientist paper covered in this class before.

**6:20** · So similar style of benchmarks.

**6:23** · In total, it covers about 170 tasks going all the way from say, one seconds to eight hours.

**6:30** · So if you were to look at this, in terms of a division, you will see that HCAST has about 97 tasks.

**6:37** · These are the 1 minute to 30 hour tasks.

**6:41** · SWAA has about 66 tasks.

**6:44** · And then RE-Bench, which are more research engineering tasks that take much longer are about seven tasks.

**6:49** · So the first they do is they collect these tasks, they vet the set of tasks that go into each of these benchmark suites.

**6:56** · Then they actually have time estimates from both human doing the task and then the agent doing the task.

**7:02** · From human runs, they actually estimate the amount of time it takes the human to complete that task, and whether they found it difficult or not.

**7:10** · And then for the agent, they're measuring whether they completed it reliably or not.

**7:14** · And finally, based on enough data points, they fit a curve which measures the success rate versus the time estimate.

**7:22** · And based on that, they find the time horizon for these models completing the tasks.

**7:27** · So that gives a sense of the horizon length relative to model release dates.

**7:31** · So what we'll see in terms of trends are, for models released on different dates, roughly what is the time horizon with which the models complete the tasks?

**7:42** · 50% of the time or ti 80% of the time?

**7:47** · Questions.

**7:54** · What is a task that takes you guys a couple of minutes?

**7:59** · And what's a task that takes you guys say a couple of hours that you think you would like to delegate to the models?

**8:12** · Writing the literature review section of the paper.

**8:15** · Yes.

**8:15** · That usually takes several hours.

**8:20** · So that would be a great task.

**8:21** · And that would fall somewhere in the HCAST or RE-Bench task.

**8:28** · Any other takers relative to what you do?

**8:32** · Yeah.

**8:33** · \[INAUDIBLE\] for each reference.

**8:36** · Say that again.

**8:37** · Double-check \[INAUDIBLE\].

**8:41** · So in the paper writing, you want the BibTeX item to be correct.

**8:45** · So you want it to go query the right websites and find the BibTeX item.

**8:49** · How many minutes do you think that should take?

**8:53** · So it falls more in that one-- the HCAST style, like diverse tasks?

**8:57** · OK.

**8:59** · Cool.

**9:02** · Any other tasks that people think that the model should be good at?

**9:12** · OK.

**9:14** · I think \[INAUDIBLE\] should be faster.

**9:26** · So refactoring the codebase can be large or can be small.

**9:29** · Yeah, it depends on what the refractor.

**9:32** · What the refactor requires.

**9:33** · If the logic stays the same and it's just moving around code, then that perhaps is a few hours can be a couple of days.

**9:39** · Someone has to check correctness of that as well.

**9:41** · Makes sense.

**9:43** · So that one will fall perhaps like closer to RE-Bench.

**9:45** · One can imagine that there will be a version of just like the coding-related tasks.

**9:50** · Cool.

**9:52** · OK.

**9:57** · So for the second step, for the human \[INAUDIBLE\], so for a certain type of task, for these types \[INAUDIBLE\] human beings \[INAUDIBLE\] some people do it faster.

**10:09** · Some people do it slower.

**10:12** · So I'm just wondering, so on one extreme case, you just have one main evaluator and then you have just one \[INAUDIBLE\].

**10:22** · On the other extreme, you have 100 generations.

**10:26** · You have distribution.

**10:27** · And you can compare where the algorithm stands.

**10:30** · So I'm just curious where that's most of the individual performance.

**10:33** · So typically, what is done with most of the-- I mean, getting a lot of experts to solve the task is relatively expensive.

**10:40** · So typically, you will have a few experts solve the task and then you look for inter-rater agreement or inter-human agreement in this particular case.

**10:48** · And what you're saying is that generally, if the numbers are very far off, then you go get more data points.

**10:53** · And if there's general agreement, then you move on.

**10:58** · So just the example of task, just related to what the class talked about, where you wanted the literature review section or you wanted the BibTeX being accurately classified or the refactoring of the code base.

**11:12** · Some of the example tasks of different durations that were in this paper are find a shell script.

**11:17** · So that's perhaps just take three seconds.

**11:20** · Or Wikipedia research.

**11:22** · This is closer to the research section that you wanted.

**11:26** · Or another one is detect and fix a bug in the input files for a simulation, so that takes like 10 minutes for a human.

**11:35** · Then there is munging of data.

**11:36** · So data munging task where you're transforming some JSON data from one format to another.

**11:40** · And then Cuda backtesting tool, which basically you are implementing.

**11:46** · Custom Cuda kernels can take tens of hours to here it's like eight hours and they are aiming for a certain performance improvement.

**11:54** · So all of these tests are part of this particular benchmark.

**12:00** · And the way-- this actually addresses the question you were asking, the way they are going about getting the human baseline for task completion is that they go and get skilled professionals with roughly five years of experience in the field to record their completion times for successful attempts.

**12:16** · And then they take a geometric mean for the task difficulty rating based on the humans that went and solved this.

**12:22** · One challenge with this is that people who are experienced in the field are conditioned to what it means to be successful in this.

**12:28** · So they will often underestimate the difficulty of the task, which might not correlate to how the model sees whether this task is difficult or not.

**12:37** · So in terms of trends, what they found is, on the x-axis, we have the human time to complete.

**12:42** · And on the y-axis, we have the success rate going all the way from 0 to 1.

**12:47** · So the model success rate for-- if you look at smaller tasks like 1 to 30 second tasks, which are the SWAA tasks or the green tasks, that's generally on the higher side.

**13:00** · For HCAST tasks, which are basically the tasks which are diverse tasks going all the way from say few minutes to several hours, that's all over the place.

**13:10** · So it's anywhere from 0.8 being the highest all the way to 0.

**13:15** · And then the RE-Bench tasks have some success, but tend to be on the lower side at this point in time.

**13:21** · There have been papers saying that they are making progress on RE-Bench tasks, but generally, it's a much harder task in terms of the human time to complete, it takes long.

**13:31** · And then the model success rate is also fairly low.

**13:34** · So the longer the task, the harder it's for models to stay on track and complete.

**13:38** · And this is partly why agentic evaluations and what you measure starts to become a challenging aspect.

**13:46** · In terms of trends, if you were to-- we chatted about the fact that if you were to query these models about 2019 when GPT-2 came out, typically, the models would really just address tasks that were two seconds long.

**14:01** · So on the y-axis, you have the task time for completion with 50% success rate.

**14:06** · So it doesn't have to be completely reliable.

**14:09** · So in 2019 when GPT-2 came out, only two seconds.

**14:14** · Closer to GPT-4, which is 2023, you're starting to see a few minutes.

**14:20** · And when we have Claude 3.7 Sonnet and o1, at that point, you're starting to see a few hours.

**14:27** · Now note that this is almost like a doubling because this is-- so it's doubling every seven months.

**14:35** · But the other thing to note here is that even though these tasks are being completed, the reliability is not high.

**14:40** · They only being completed 50% of the time.

**14:43** · So that's like saying that you gave your task to an intern, but it only completes it 50% of the time.

**14:48** · So it might come back with an answer or it might not.

**14:51** · So there's always some amount of uncertainty.

**14:55** · So this is just making the same point that going from GPT-2, which was just two seconds to GPT-4, which was like eight minutes, now Claude 3.7 Sonnet in 2025 can go all the way to 59 minutes with 50% success rate.

**15:10** · And what is really driving this improvement?

**15:13** · So some of the capabilities that we're seeing in the model that are really helpful in terms of driving these improvements are better logical reasoning.

**15:22** · So the models can-- we've covered a lot of previous lectures on the models learn how to reason better.

**15:28** · So the reasoning capabilities definitely drive some of these improvements.

**15:33** · Code generation capabilities have improved.

**15:35** · So we have covered several lectures where you've seen the models do better on the code generation side.

**15:40** · So that's definitely driving some of these improvements.

**15:43** · Too use.

**15:43** · So we covered React and several papers around just how the models use tools.

**15:48** · So that also has added up.

**15:50** · And then in general, there has been a focus on getting these models to be more reliable so that they're not repetitive in just repeating the same behavior over and over again.

**15:59** · And finally, you want these models to generally recover from errors.

**16:03** · I mean, if you're going to do an eight-hour task, you're going to have some steps which are going to be wrong.

**16:08** · So you have to recover from those errors, and you need a better awareness of, what is your final goal?

**16:13** · And some notion of state of or memory of, what is the final goal?

**16:18** · And how far along are you in terms of making progress towards that goal?

**16:23** · Other aspects of what folks have seen as driving these improvements.

**16:27** · Any comments?

**16:32** · Why do you think Claude Code does better today relative to say, last year?

**16:40** · How many people use Claude Code or Codex?

**16:43** · There's a new trend for context engineering.

**16:45** · People are just learning how to structure the context better, so that the tooling just becomes better and improves to make the improvements.

**16:54** · So what you're saying is, I'm just repeating for the class, that context engineering or being able to structure the context better over multiple time steps is starting to improve, which also helps.

**17:05** · Thank you.

**17:06** · You see that compaction window that happens when Claude basically gets to the end of its context.

**17:14** · Yes.

**17:15** · I think just like maybe from feedback of actual people using it.

**17:18** · And then I know that for a cursor, they have online URLs, right, for tab completions.

**17:25** · So maybe, I don't know for how that works with board for Claude Code, but I guess, supposedly they get some sort of feedback from the user logs and then try to either back-propagate \[INAUDIBLE\] or just kind of figuratively in the workflow.

**17:40** · So generally, address the class of problems that are starting to show up.

**17:48** · Yes.

**17:50** · So when problems \[INAUDIBLE\] So when problems are really complex now is the coding agents usually trigger explicit planning stuff.

**18:04** · So that kind of helps to plan when problems are re-occurring.

**18:08** · And so they stick to the plan.

**18:09** · And this kind of reduces some trial and error with experience.

**18:14** · Nice.

**18:15** · So what you're saying is that if you look at where the problem is very complex, the model as a first step does some planning.

**18:21** · So it breaks down the problem into multiple steps.

**18:24** · And oftentimes, when it goes and executes some of the steps, it might actually trigger re-planning.

**18:29** · So it might actually come up with a new set of steps to go do based on the data it's collected.

**18:36** · That's very good insight.

**18:38** · So when you use Claude Code, sometimes the code has anger.

**18:44** · I mean, the Claude Code, it seems the code that has a problem.

**18:48** · So it's \[INAUDIBLE\] the user may use \[INAUDIBLE\] copy paste the code, the editor to the Claude code and them Claude Code will know that code has \[INAUDIBLE\].

**19:02** · So that means that \[INAUDIBLE\] it's similar to \[INAUDIBLE\].

**19:06** · Yes.

**19:07** · So there's always the user feedback where the user says what you gave me is not right.

**19:11** · So then the model has to redo the job.

**19:15** · That's same as doing like someone has given you an assignment.

**19:18** · And then if it's not to the satisfaction, you've got to redo.

**19:23** · That's fair.

**19:24** · How does memory play out in all of this?

**19:27** · Or context, what's in context?

**19:32** · We covered, like we had a whole lecture on memory.

**19:36** · Why is memory important?

**19:39** · OK.

**19:40** · So sometimes the agent has like atomic memory knows \[INAUDIBLE\] about understanding of code base.

**19:46** · So this kind of sampling from theory and updating the \[INAUDIBLE\] priors, so it knows better like what the environment looks like \[INAUDIBLE\] expected.

**19:56** · OK.

**19:57** · So what he's saying is that sometimes the agent might actually need to understand what the environment is better.

**20:04** · So for example, an understanding of the code bases.

**20:06** · So having memory helps keep that understanding if it's going to operate over a similar code base.

**20:12** · OK, thank you.

**20:15** · OK, let's keep going.

**20:18** · So now let's take a look at reliability aspect of it.

**20:21** · So capability is only one axis along which we want these models to do better.

**20:26** · Reliability is the other one.

**20:27** · So what we are measuring here is again x-axis is the model release date.

**20:32** · And now we want to see how the models do at 80% success rate.

**20:35** · So the gray line is the 50% reliability one.

**20:38** · And then the blue line is the 80% success rate.

**20:42** · And y-axis is the time taken by the models to complete the tasks.

**20:48** · So what you see here is that while we were claiming that you can get all the way up to 59 minutes in 2025 with the latest and greatest models, if you want high reliability, you are still at a few minutes or maybe tens of minutes.

**21:02** · And so to get 80% success rate with the models, there is a big delta between the 59 minutes that we were claiming with the best model versus at 80% success rate, you're still closer to say, somewhere around 8 to 10 minutes.

**21:17** · So big delta roughly tells you that there's a lot of headroom to make in terms of reliability so that the model comes back and is successful most of the time.

**21:30** · Yes.

**21:31** · So do you \[INAUDIBLE\] based on your experience?

**21:35** · Let's ask that question at the end of the lecture because you will have a lot more-- I mean, the whole lecture was about this.

**21:43** · I just wonder what paper is this part from?

**21:47** · This is from the paper-- paper is posted online.

**21:50** · The first paper, right?

**21:53** · Yeah.

**21:54** · Both the paper and the slides are online.

**21:59** · So basically, 80% horizon is still showing doubling time, similar time horizons.

**22:07** · But it is saying that you have-- it's five weeks shorter.

**22:11** · So the 15 minutes is what Claude 3.7 can achieve 80% of the time versus 59 minutes 50% of the time.

**22:18** · So this gap, basically, says that if you're trying to deploy these models in real-world tasks, then there will be reliability challenges even for moderately complex tasks.

**22:27** · So that requires-- there's definitely a lot of headroom in how we build systems on top of these models.

**22:35** · And an important question to ask is, what are the kind of failures that we run into with these models?

**22:41** · And this is looking at both GPT-4, which is a non-reasoning model and o1, which is a reasoning model.

**22:46** · Now this paper is a bit older and you can refer to things that are a bit newer.

**22:50** · But at the same time, the kind of failure modes are very similar in many cases.

**22:55** · So we can take a look here.

**22:56** · So the kind of failure modes that they found are closer to either poor planning.

**23:01** · So the model doesn't know how to break the task.

**23:04** · It was given down into steps.

**23:07** · Poor tool choice.

**23:08** · So the set of tools that it tries to choose here may or may not be correct.

**23:13** · And there were errors along both these axes in the GPT-4 and o1.

**23:19** · A second failure type is incorrect mental math or reasoning.

**23:22** · Style tasks.

**23:23** · So here the model is basically doing some sort of math or reasoning, but it's doing it incorrectly.

**23:29** · Another failure type is that prematurely, it abandons the tasks because it goes around some repetitive behavior, but is not quite able to figure out what it means for the task to be successful.

**23:40** · Another failure mode is that the model will basically get into a repetitive loop, so it will basically go do some actions.

**23:47** · And then that's still the highest probability action even after it has failed.

**23:51** · So it then goes and does that action again.

**23:54** · So it might basically be with high probability repeating the same action.

**23:57** · So with GPT-4, this was a pretty high.

**24:00** · For o1, this has become lower.

**24:03** · And then there's other category of tasks that they showed-- there are other categories of failures that they showed are also prevalent.

**24:10** · But this gives you a sense of planning, tool choice, reasoning errors, not being able to figure out when the task is completed, and then just repetitive loops tend to be some of the failure modes for these models.

**24:23** · And failure mode analysis is very useful in understanding where the models can or cannot improve.

**24:32** · This is a common way, is that typically \[INAUDIBLE\].

**24:39** · Yes.

**24:40** · \[INAUDIBLE\] Not similar categories, but it's common to evaluate the models.

**24:46** · And then if you're saying that you have a challenging benchmark, then you would showcase, where do the models fail?

**24:52** · What is the common failure pattern?

**24:55** · \[INAUDIBLE\] Human reader or self-inflicted pain.

**25:03** · So you evaluate the model yourself and see where it's failing.

**25:07** · I think we have been asking you guys to do that for homeworks.

**25:11** · When you go actually try to do the self iterative refinement loop, then you have to evaluate where the model failed.

**25:21** · OK.

**25:22** · So some of the challenges in this benchmark.

**25:25** · So no benchmark is ever perfect.

**25:28** · Every benchmark has some challenges.

**25:30** · So some of the things that \[INAUDIBLE\] did get right is that it's the first attempt at measuring, what is the time horizon of tasks that these models can complete?

**25:39** · And some of the challenges that the model does not quite solve is that it has lower performance on tasks that are messy, where there's not one single correct answer or there is some amount of complexity involved.

**25:53** · But if you have some amount of messiness then, similar trends will be there at in different categories of tasks.

**26:02** · Another one is that if you try to look at SWE-bench, SWE-bench has a similar trend to what we were showing in all the plots before, but the annotators generally underestimates SWE-bench.

**26:16** · And the models also have seen most of the GitHub repositories.

**26:19** · So a lot of the estimates that are made on SWE-bench tend to be shorter in terms of doubling time relative to if it was a completely unseen repository.

**26:30** · A third challenge with the benchmark is that if you actually have internal pull requests-- so this is for internal code bases, then what has been found is that if you put contractors on the job, people who don't have context, who have not been working on that code base, versus you put code maintainers on the job.

**26:48** · The contractors can be anywhere from 5 to 18 times slower.

**26:52** · And model performance is consistent closer to contractor times because it's basically never seen that code base before.

**26:58** · So this suggests that when you're dealing with these models going and solving these tasks, this is still very valuable.

**27:06** · But at the same time, it's operating more as not someone who is an expert in that area or has the context of that area.

**27:13** · It's more as a low context human who's basically been asked to solve that problem, similar to a contractor.

**27:21** · So that's summarizing the first paper.

**27:25** · But hopefully, that gives you a flavor of when we are measuring the progress in AI, one of the axes in agentic evaluations that becomes important is to measure, how long are the tasks that the AI can complete reliably?

**27:40** · Any questions or comments before we move to the next section?

**27:51** · OK.

**27:53** · So the next paper that we will look at is GDPVal, which is evaluating the model performance on real-world economically valuable tasks.

**28:01** · So instead of asking the question, can AI do this?

**28:05** · Where you have a task that you want to delegate to AI.

**28:08** · Hear the question is very much around, if we were to give this task to the model instead of a human, is the output good enough?

**28:16** · And the win rate will be directly against industry experts.

**28:20** · So it will actually take-- the task suite is designed as real work from professionals who have more than a decade of experience in their fields.

**28:29** · So you will see here that the kind of professions that were used for task suite design are pretty broad ranging here.

**28:36** · So it goes anywhere from say real estate, where you take a broad range of tasks to government to manufacturing, professional, scientific, and technical services, healthcare, finance, retail, wholesale, and information, including film and video editors.

**28:52** · So it's actually a pretty broad range of tasks.

**28:54** · And given the models have become multimodal, this is does make sense.

**29:00** · The models will not be good at all of these tasks.

**29:02** · They will only be good at some of these tasks, of course.

**29:06** · So let's take a look at some example tasks here.

**29:09** · And also think about the tasks that you think that the models might be good at as you go through this list.

**29:16** · So in manufacturing engineer, it's being asked to design a 3D model of a cable reel stand for assembly line.

**29:24** · In financial and investment analysts, it's being asked to create the competitive landscape.

**29:29** · So it's a research heavy task.

**29:31** · In registered nurse, it's basically assessing the images of issue and creating a consultation report.

**29:40** · In film and video editor, it's asking to create an intro reel given some sort of script.

**29:48** · In customer service, it's being asked to draft an email response for dissatisfied customer.

**29:56** · In concierge, it's basically creating an itinerary for a family of four.

**30:01** · In audit, it's basically figuring out pricing inconsistencies between given a few different purchase orders.

**30:09** · For a real estate agent, it's designing a sales brochure for a new property.

**30:13** · And then recreation worker, it's basically asked to optimize the layout of vendor fair?

**30:22** · What do people think?

**30:24** · These are very real tasks, actually sourced from professionals in their fields.

**30:30** · Very interesting, right?

**30:32** · May things are very subjective to evaluate.

**30:36** · Very subjective to evaluate, yes.

**30:38** · \[INAUDIBLE\] I mean, what I do is going to may not be what you do.

**30:42** · Yeah.

**30:43** · So that's why the success metric will be win rate.

**30:46** · It's not like if you put humans on the job versus you put models on the job, what is the win rate?

**30:51** · And there might be specific style that the model chooses that doesn't quite hold for all cases.

**30:58** · Yes, so it's objective.

**31:00** · And at the same time, that subjective nature also makes one of the challenges.

**31:05** · That's why real-world work requires both context and subjectivity in how things get evaluated.

**31:13** · What are other real-world tasks that people have seen that are interesting related to this?

**31:20** · You brought up about-- you put private Wiki QA and use that to query the knowledge base in your job?

**31:29** · That's feeding into coding even, what we're finding is actually better finding dead parts of the Wiki that are no longer useful \[INAUDIBLE\].

**31:41** · Thanks.

**31:47** · Any other ideas from the class?

**31:51** · \[INAUDIBLE\] Other tasks, yeah.

**31:54** · So doctors-- no, I mean, it has no respect.

**31:58** · I feel for controversial topics is not there.

**32:00** · For example, \[INAUDIBLE\] or other \[INAUDIBLE\] based on those context are following requirements.

**32:12** · So I think \[INAUDIBLE\] here.

**32:15** · For example, there are tasks-- I think we should separate out.

**32:18** · There's definitely a question around whether the models are good at it and whether we want to use them for ethics and actual compliance reasons.

**32:27** · So I think those two questions need to be separated out from what models can do today.

**32:34** · So this is more about, is the model output good enough in the subjective areas?

**32:39** · I'm trying to see if our doctors-- so there's registered nurses.

**32:44** · There's a lot of tasks.

**32:45** · But they put registered nurses and nurse practitioners in healthcare more than doctors.

**32:50** · What about for people \[INAUDIBLE\] for the information science, they don't mention like computation.

**32:56** · Say that again.

**32:57** · Compose a song, compose a song for someone.

**33:02** · OK.

**33:04** · So yes, that's correct.

**33:07** · So maybe that's an emerging task that will show up.

**33:09** · But that's not part of this benchmark just yet.

**33:13** · Here's one comment on that.

**33:14** · Maybe for the music, composing music, the verification is quite subjective, or it's harder to say, I guess, you can make \[INAUDIBLE\] music and all of them, it's hard to differentiate.

**33:26** · And maybe whether you're trying to hear is it, so that they can-- there is a deliverable that's fairly clear if it is working or not.

**33:40** · So top-down, this dataset, this evaluation dataset targets about nine sectors.

**33:46** · And they actually went for top 5% of the GDP.

**33:49** · So they're asking, what are the most economically valuable tasks?

**33:52** · And whether the models are good enough at that.

**33:54** · They cover about 44 occupations and sourced about 1,320 tasks through that.

**34:01** · And 200 of them or 220 of them are actually in an open goal set that is on hugging phase.

**34:07** · Predominantly went for digital tasks.

**34:09** · So tasks on computer which is 60% of the-- so O\*NET is a taxonomy of all tasks that are related to occupations.

**34:20** · So 60% of the O\*NET tasks that are computer-based and digital made it into this evaluation dataset.

**34:28** · And this basically is a pretty representative coverage of various set of tasks that an occupational expert will need to do in these particular sectors.

**34:39** · And in terms of the characteristics of tasks that people went after, they might have as long as seven hours of completion time on average, but some might require weeks.

**34:52** · The tasks were both text-based and multimodal.

**34:54** · So like CAD, video, audio, spreadsheets, presentations.

**34:58** · The average value of the task, at least in the gold subset, was anywhere from say $400 per task.

**35:04** · But if anyone has seen cvLancer, there's also much higher value tasks.

**35:09** · So this one also has high value and low value tasks.

**35:12** · Many of these tasks, about 70% of these tasks, require interaction with the reference file.

**35:17** · So you have to interact with some reference files to arrive at a final output.

**35:22** · And all of these tasks were vetted through experts.

**35:26** · So about 89% of the tasks were actually vetted by experts as being very well specified.

**35:32** · So they were not like ill specified and extremely hard for the model just because they're ill specified.

**35:38** · So if you look at the trend, so on the x-axis, now you see different models all the way from GPT-4o to GPT-5 high to Claude Opus 4.1.

**35:49** · And on the y-axis, you're looking at win rate versus the industry professionals.

**35:55** · So basically, if you had an expert with more than a decade of experience solving it versus the model solving it.

**36:01** · So light blue is wins plus ties and dark blue is wins only.

**36:05** · There's a pairwise preferences.

**36:07** · So if you look at GPT-4o on an average, the average numbers don't mean that every single task was solved like that.

**36:15** · Go anywhere from say 12.4%, so that's 2024, to it starts to get to 25.

**36:22** · And then more recently, it is in the 30s.

**36:24** · And then now with Claude Opus 4.1, it starts to get to 47.6.

**36:29** · So that's a very different trend compared to METR where we were talking about this doubling trend every seven months.

**36:35** · It's more of a linear trend roughly compared to the exponential trend that METR was talking about.

**36:40** · And at the same time, this is real work where you are comparing relative to an expert.

**36:45** · So the measurement is very much based on whether this task, whether the model output was good enough or not.

**36:50** · So the reliability or rather the model output being useful matters here.

**36:57** · Questions.

**36:59** · Yes.

**37:01** · This trend is directly comparable to the meter one, though, because here the y-axis win rate for industry professionals as opposed to the time horizon that's in the other case.

**37:17** · So yeah, should I really think about them as disagreeing?

**37:22** · I wouldn't say that disagreeing was wrong because they're measuring different metric, as we said early on.

**37:27** · But I think what it's roughly emphasizing is that when you see an exponential trend, people often assume that OK, so now AI can do one hour.

**37:38** · So next, it will be able to do a couple of hours.

**37:40** · And the next, it will be able to do a couple of days.

**37:42** · So there's that exponential trend that gets people.

**37:46** · What this is saying is that if you look at tasks that require say several hours or a couple of days or a couple of weeks, then the models are only so reliable in doing that and it's actually breaking it down by profession.

**37:59** · So it kind of makes it more realistic by nailing it down not just by numbers of hours, but more by this is real work.

**38:07** · And can the AI models do it or not?

**38:13** · Other comments?

**38:13** · Yeah.

**38:14** · I think this chart is like on the aggregate level across all the professions.

**38:18** · We will look at the specific ones as well.

**38:20** · So there might be maybe ones that are more susceptible, where, I guess-- Another set of comments with respect to, say, the model-specific trends is that it always tends to be better at, say, aesthetics, document formatting, understanding PDFs, spreadsheets, and presentations, while GPT-5 often tends to be better at, say, instruction following, correct calculations, and just text-based tasks.

**38:45** · So that's something that was noticed by this particular evaluation.

**38:50** · And then if you look at failure modes, which is very important to analyze in most of these benchmarks, then oftentimes the common area failure ends up being instruction following.

**39:00** · So a lot of the blue bars show different instruction following errors in different models.

**39:07** · Oftentimes, the models will promise to look at the reference data, but then actually not look at it.

**39:14** · They will override it with whatever hallucination they want to come up with.

**39:17** · And then there's also formatting errors that tend to be a bit of a problem, with, GPT-5 tends to have fewer instruction following error is what was measured by this particular benchmark.

**39:30** · Related to the reference data, so our next particular section of the lecture will actually discuss more about that, being able to consult a knowledge base or reference data and why that's an important skill to go test.

**39:47** · And then in terms more on the failure modes.

**39:50** · So this was basically measuring whether GPT-5, if you look at the percentage of tasks that will generally be seen as acceptable but subpar, if you delegated that task to the model.

**40:00** · What they found was that roughly half the tasks were acceptable, but subpar, but then only 20% of the tasks fell somewhere like OK, the model will genuinely be better.

**40:13** · And 29% of the tasks were like bad or catastrophic, where the model output was really not acceptable at all.

**40:20** · And there was some amount of disagreement between human graders with respect to whether they agree on what the assessment of the model output is or not.

**40:30** · So that also affects some of this analysis.

**40:34** · And then another interesting thing is that it's something that since this is a self-improving agent's class, so a lot of times if you basically do parallel sampling.

**40:45** · So if you try something or sequential sampling where you do something n times, then ask the model to fix itself based on whatever it was seeing.

**40:53** · That loop can often really improve.

**40:55** · So what this particular table is showing is that you can either do naive just one trial or you can do-- sorry, you can try one time or you can try n times where you basically, every single time you do something, you can improve the last iteration.

**41:10** · So in terms of speed improvement, what they found was that GPT-5 was overall about 1.6x in cost improvement if you could try n times and about 1.4 in speed improvement relative to an unaided expert.

**41:24** · But there is still where it's successful, it is still less than 10% of the human expert salary.

**41:30** · So there's definitely some subset of professions where the models are doing a pretty strong job and have the capability to take on that tasks completely.

**41:41** · So some people also mentioned exactly which category We will get that.

**41:48** · That's exactly where we're going.

**41:51** · So in terms of performance variation.

**41:54** · So by sectors, in government, retail, and wholesale, I think the broad items, the broad categories are not that illustrative.

**42:02** · Looking at the a specific task help.

**42:04** · But they are the-- performance was near parity relative to human experts.

**42:09** · By duration, the models were better at shorter tasks up to a few hours, definitely declines with longer tasks.

**42:16** · And we already discussed that on modality.

**42:18** · There were some models were better at multimodal while others were better at text.

**42:23** · OK, this is going to be an extremely dense plot, but I think the thing to notice here in all of these plots is that the red line is the one where we are saying the human experts and then all of these different colors are corresponding to different models.

**42:37** · So if you look at places where the models are better or at least are almost at par with the human experts, you see that counter and rental clerks.

**42:46** · So some of those tasks have already started to hit that.

**42:49** · Real estate brokers, for example.

**42:52** · Shipping, receiving, and inventory clerks, for example.

**42:55** · Buyers and purchasing agents.

**42:57** · You can imagine why.

**42:59** · Computer and IT managers are definitely like it's starting to hit where an average human expertise would be.

**43:06** · When I say average this is not like the best expert in the field.

**43:11** · And then software developers definitely are.

**43:13** · A lot of the models are starting to hit capability in typical software engineering tasks.

**43:19** · I'm seeing some interesting reactions from students in class.

**43:25** · Can I have some comments?

**43:27** · For the software, I know that you mentioned previously, it's like \[INAUDIBLE\] 14 years of experience.

**43:34** · But software developer, it can be-- like the range can be pretty wide.

**43:42** · I think in the case of software developers, they probably went for more of the maintenance of the repository as opposed to the decade of experience.

**43:48** · I think there are fields here where, I mean, for example, industrial engineer or mechanical engineer, the decade of experience matters.

**43:55** · And software developer, knowing the software codebase in and out.

**43:59** · And the then two cases of that \[INAUDIBLE\].

**44:05** · OK, this is another one of those thoughts.

**44:07** · Let's just focus on where we're seeing the models do extremely well.

**44:12** · So again, government, the administrative service managers, in compliance officers, models are doing extremely well.

**44:21** · And then in medical and health service managers, those tasks, multiple models are doing extremely well.

**44:27** · In personal financial advisor and customer service representatives also, you're starting to see that the models are starting to do extremely well.

**44:34** · But in general, this gives you a glossary or a taxonomy set of tasks that the models are starting to perform well in.

**44:41** · And if you're looking at other tasks where the models are failing, I think this is a very good way to get a starting point on, what are the models failing at?

**44:52** · Questions or comments?

**44:54** · OK, this is the last round, I promise.

**44:57** · So first line supervisors and retail sales workers.

**45:00** · I think in general, in retail trade, we are starting to see some of those tasks taken on by the \[INAUDIBLE\] as a useful thing for non-retail sales workers.

**45:11** · So in general, on the sales side.

**45:13** · In terms of editing tasks, we're seeing the models do extremely well.

**45:17** · In terms of research-based tasks, both investigative and detective-based and news analysts, and then sales representatives, wholesale and manufacturing, those tasks seem to suggest that the models are doing extremely well.

**45:34** · So this gives you a flavor of the kind of tasks that the models are performing strongly at.

**45:40** · Overall, if you under-specify the prompts.

**45:43** · So if you actually remove context from the prompt, then the models do end up not doing that well.

**45:49** · In their particular case, there was a few points lower in terms of win rate.

**45:53** · But in terms of actual model output, the models actually struggle to figure out what to work on.

**45:58** · So there's definitely some amount of-- when you're doing real work and you can specify all the context that the human had in their head to go do the work.

**46:06** · And it's mostly about reasoning and just going and executing a certain set of tool calls, then the models can do the job.

**46:12** · But there's a lot of figuring out what needs to be worked on, how that context needs to be used, what needs to be in the context.

**46:19** · And a lot of that doesn't get captured by the model on its own.

**46:23** · So that's definitely one area where the humans have to orchestrate, what is it?

**46:28** · What is the actual thing to go work on?

**46:34** · So humans are basically architecting, what is the set of problems?

**46:38** · And then the model can go solve it in certain cases.

**46:44** · And this is further exemplified by what we covered before where if you had a repository maintainer versus an external contractor, the speed at which the repository maintainer is able to solve problems is generally much faster.

**46:55** · So if you have an expert who has a domain knowledge, they will generally be faster compared to someone who has no context.

**47:02** · So real work is often context heavy.

**47:05** · And what we are measuring in this particular evaluation is more around, can a smart person do this?

**47:10** · Or can someone embedded in this work can do this?

**47:12** · But if you have to go get context for that task that models are not yet able to do, and this evaluation is not measuring that.

**47:22** · So in near term, what this means is that AI assistance is already happening in professional workflows.

**47:27** · We have covered some of the agentic workflows in early parts of the lecture.

**47:31** · And it's definitely cost effective when you couple it with human oversight, like if the humans are architecting what the models need to go work on, the AI assistance is definitely helping.

**47:41** · In certain occupations, this is more impactful than not.

**47:46** · But you do have to choose different models, and different models are stronger at different task types as well.

**47:53** · OK, questions or comments.

**48:02** · Yes.

**48:04** · How much \[INAUDIBLE\] on the actual dollar value \[INAUDIBLE\].

**48:11** · So the tasks?

**48:12** · Yeah.

**48:15** · Why do you ask that question?

**48:18** · Well, because it seems like it's a relevant way of quantifying actual economic impact.

**48:27** · You can say, oh, AI can now do $100,000 of work or something that.

**48:34** · But if these numbers are collected in a way that seems unreliable or misleading, then \[INAUDIBLE\].

**48:46** · I think to me, it's not so much about the dollar.

**48:49** · I mean, they did go after the top 5% of the GDP tasks.

**48:53** · For the past several decades, the knowledge work has been one of the key areas that has been the highest paid profession.

**49:00** · And in knowledge work, there are certain categories of tasks that the models will be very good at.

**49:06** · Deep research being one of them, perhaps, another one being like code generation.

**49:11** · So in each-- or understanding a diverse set of information sources.

**49:15** · So the models will generally be good at those set of tasks.

**49:18** · So I think the question I would ask is, what is the category of tasks that the models are likely to be good at?

**49:24** · Just because at any given point in time, humans are strong at certain set of things.

**49:28** · And machines, just by way of being able to crunch the electricity, are just better at certain set of things.

**49:35** · So this is more along those lines.

**49:38** · So there's a certain category of tasks that will definitely be valuable.

**49:44** · Delegating to the model is the way to look at it.

**49:46** · And which are the professions in which those category of tasks fall?

**49:50** · Is what this benchmark is showcasing.

**49:54** · Before this benchmark came out, people would talk about this area of like OK, this is going to impact a lot of professions, but there was no quantitative way to measure what set of tasks in each of these professions.

**50:05** · And it seemed like a humongous task to go do that.

**50:07** · So this is a very verifiable, quantifiable way to even have a taxonomy to list the set of tasks in each of the professions.

**50:16** · And what does it mean for the model to go do them?

**50:19** · Earlier, when we were doing the class, in the previous iteration, we were only talking about ML-Bench and RE- Bench and given that.

**50:26** · Our backgrounds are, say, more ML or more research or more software.

**50:30** · It's easier for us to understand the progress of these models in those domains.

**50:41** · I'm just curious, how is \[INAUDIBLE\] when the model will outperform the human, it just means like it's human, not necessary \[INAUDIBLE\] anymore.

**50:54** · I mean, this is where I was adding these caveats.

**50:57** · So when a model is outperforming the human, you should go look at the prompt.

**51:02** · And what that's saying is that for a human who has a lot of context, if they were to specify all the context in their head to specify it in a prompt, then the models can also do those tasks.

**51:15** · While a lot of actual work experience or a lot of workplace challenges often are about figuring out what to prioritize, what are the set of problems to solve, where to put our resources.

**51:34** · We will move to the last benchmark, which will be focused on DeepScholar-Bench.

**51:40** · This was a task that one of our classmates requested early on, where they want AI to write the literature review section of their paper.

**51:48** · So here we are.

**51:49** · Let's benchmark that task.

**51:52** · This was written at Stanford.

**51:54** · And this is basically measuring the question of, instead of asking how long will the task take to solve, is the model output good enough?

**52:05** · They're actually asking, can AI perform deep research synthesis?

**52:08** · Can I go study a bunch of references and retrieve the relevant information and then synthesize the findings into a coherent set of reports and have verifiable citations?

**52:19** · And there have been several industry prototypes that have come out.

**52:23** · So there's OpenAI deep research, Gemini deep research.

**52:26** · Perplexity has a deep research thing.

**52:28** · Storm is from Stanford.

**52:30** · There is OpenScholar.

**52:32** · You folks built a deep research agent in homework 3 and maybe you got a flavor of what that feels like.

**52:38** · So in general, there has been a lot of research activity in this area, and it still continues to be a challenging area, as what this paper shows.

**52:49** · So the task that this paper addresses is to generate the related work section for academic papers.

**52:55** · The reason they care about this task is because this is a task that most of us require when we are writing papers.

**53:02** · And it requires continuous updates with fresh queries.

**53:04** · So there is not no staleness.

**53:07** · The way they went about constructing this dataset is they used recent arXiv papers with PhD level difficulty across 22 domains.

**53:15** · And they rerun it monthly with new papers, so it stays live.

**53:20** · So it's very nice in that respect as well.

**53:23** · And it avoids data contamination.

**53:26** · They only look at papers that are post-training of a major model.

**53:32** · So that's very nice.

**53:35** · What they're evaluating the models on is three particular axes.

**53:38** · So the first thing they're evaluating the model on is knowledge synthesis.

**53:41** · So what they're basically saying that, is the model output organizing and is coherent in organizing the knowledge that is presenting?

**53:49** · And is it capturing all the key facts?

**53:51** · So is it capturing the key nuggets?

**53:54** · This second axes, it's evaluating the model on its retrieval quality.

**53:59** · So if it's looking at a particular set of references, how relevant they are to what you wanted to do research on?

**54:07** · For example, if you're writing a related work section for your final project, and you have say, 10 references that this model or agent went and fetched, are they relevant to what you actually want to present in your final report or not?

**54:25** · Citation counts.

**54:27** · It's kind of well known that you want highly authentic sources.

**54:30** · So whether the papers are important in terms of covering those in the retrieval and then reference coverage.

**54:37** · So this is similar to-- is it finding important papers or not?

**54:42** · And then the third axis it's measuring is verifiability.

**54:46** · So, do the citations support the claims?

**54:49** · So even if it finds good papers and it's citing some aspect of that paper, is the claim supported by that citation?

**54:58** · And then, are claims backed by the citation?

**55:00** · So these two are very similar.

**55:02** · But one is measuring precision and one is measuring coverage.

**55:06** · And each of these metrics are actually validated by humans.

**55:10** · So they got about 70% to 80% of human agreement when they got humans to evaluate this.

**55:18** · Now the fun thing is that most benchmarks get saturated.

**55:21** · So when we look at benchmarks, we are like, OK, well, it's already at 70% or 80%.

**55:25** · So there is no headroom.

**55:26** · The fun thing about this particular benchmark is that none of the existing systems actually exceeds 19%.

**55:32** · So if this were to show up in your homework for the next iteration of the class, there's a lot of headroom for you folks to actually make it a final project.

**55:40** · In terms of, if you look at each of these axes on which they are breaking down the model performance, in terms of knowledge synthesis, they found that OpenAI deep research does a pretty good job, but almost all of the models consistently miss key facts.

**55:55** · So even though they write coherently.

**55:56** · So it's great English, but not necessarily covering all the key facts.

**56:01** · The retrieval quality tends to be overall OK.

**56:07** · So all systems currently struggle to find comprehensive and important set of sources.

**56:12** · The document importance in all of them is less than 12.5%.

**56:17** · And then finally, if you look at verifiability, they found that say DeepScholar base got up to 90% precision.

**56:27** · But OpenAI deep research has lower verifiability, despite the fact that it does a really good job at writing really nice English.

**56:34** · So the synthesis is extremely coherent.

**56:40** · Now, if you look at the failure modes, and that's where a lot of the learnings lie.

**56:46** · Typically, the failure modes come from not finding comprehensive sources.

**56:50** · So even when they do find relevant documents, they're not always finding the foundational papers.

**56:55** · So this is where if you are an expert in the area, you kind of know from experience that there are all these foundational papers because you build that context and bookmark all the important papers.

**57:07** · The deep research agents do a reasonably strong job, but they struggle to assess the document importance beyond whether it's relevant to the context or not.

**57:16** · The surface essential facts.

**57:17** · So even with good retrieval, they don't always extract the key information efficiently.

**57:22** · If you do give the perfect sources, so even if you say that OK, here are all the papers that should have been included.

**57:29** · Even then, if you try to get them to extract the key facts, even then they get about 50% coverage.

**57:34** · And without knowing the exact papers, they get lower coverage.

**57:39** · And then finally, if you're trying to balance out the synthesis quality versus verifiability, none of the systems actually excels at both the quality of synthesis and the verifiability in certain ways.

**57:51** · So you can see that being able to refer to reference data in the agentic evaluation tasks is a non-trivial problem.

**58:00** · So it's not just about how long the task is or whether it's real world economic value or not.

**58:04** · If you have to reference some reference data to go look at, it's non-trivial because you might not get the context that an expert has.

**58:12** · So you might not have that much foundational knowledge available.

**58:15** · It might not extract the key information well enough, so it does something.

**58:19** · So it's good with human AI assistance.

**58:22** · And the verifiability with respect to citations may not have the right precision recall trade-off that's acceptable for that occupation.

**58:33** · So that roughly means-- so this is transitioning to summarize across all the papers.

**58:38** · But before I go there, let me open up for questions just on the DeepScholar-Bench style of tasks.

**58:46** · Any questions or comments?

**58:53** · Yeah.

**58:55** · \[INAUDIBLE\] seems like a much more specific narrow thing than the other two.

**59:01** · Why talk about this one in particular as opposed to any other \[INAUDIBLE\]?

**59:08** · So I think the broad theme of the lecture was very much focused on, what do we care about in agentic evaluations per se?

**59:17** · So we covered about the length of the tasks.

**59:19** · We talked about the economic value of the tasks.

**59:22** · But for real-world tasks to be meaningful, we do have to look at knowledge bases in useful ways.

**59:27** · So this is a representative task for that category.

**59:36** · Also for the most foundational papers, so I guess like for the benchmark, there's a list that's collected from human experts.

**59:45** · These are the papers that people with the PhDs think the model should hit.

**59:52** · And then you are trying to see how many were actually retrieved or whatever like by the model being tested.

**1:00:01** · I mean, at any given point in time, they're basically saying yes, so there's the human aspect of here are the list of papers that are there.

**1:00:09** · But they're also looking at whether it's-- I mean, it's not just the number of the set of papers.

**1:00:16** · It's also talking about, are you supporting if you want to make a set of claims, when \[INAUDIBLE\] section, you're answering the question of, how is this work related?

**1:00:24** · So you want to make a set of claims.

**1:00:26** · My paper is different from these other papers.

**1:00:28** · And let's say they agree on a set of topics with the model.

**1:00:30** · You still have to make a bunch of claims.

**1:00:32** · And then you have to look at the citations and back those claims up and then say that your paper is different in this particular regards.

**1:00:38** · And then this is what being covered by the field.

**1:00:40** · So, even though the key information coverage and then which papers get referenced for those claims don't have sufficient coverage in some ways.

**1:00:51** · So it's both retrieval quality and then what gets written down in terms of the key facts.

**1:01:00** · Does that make sense?

**1:01:03** · So let's try to summarize across a different set of tasks.

**1:01:08** · And this is kind of also addressing the question that our classmate asked.

**1:01:13** · So in the time horizon sense, research synthesis tasks can be anywhere from 30 minutes to 8 hours.

**1:01:22** · But the current capability range is somewhere around 50 minutes.

**1:01:25** · But the quality of this horizon might still be poor.

**1:01:28** · You might still end up with, say, 50% success rate.

**1:01:31** · So what this is roughly saying is that if research synthesis tasks are in long horizon in METR, and even though they look good on that plot, they might not be high quality.

**1:01:45** · In terms of economic value, I mean, research synthesis tasks show up in say financial research.

**1:01:52** · They show up in a lot of different research tasks.

**1:01:56** · So they have clear economic value, but they definitely require capabilities that current models are not always hitting.

**1:02:03** · And oftentimes, the gaps are coming from, say, multi-step reasoning, from being able to do a comprehensive job at information gathering to maintain verifiability while you're synthesizing this information.

**1:02:14** · So if you remember from homework 3, when you basically combine information from multiple different agent calls, you still have to maintain a certain amount of verifiability.

**1:02:22** · And then you're combining the context.

**1:02:25** · So there's context engineering from a distributed set of sources.

**1:02:28** · Maybe you did a bunch of different tool calls.

**1:02:30** · Maybe you went and redid the tool calls.

**1:02:33** · So all of that information means you have to maintain the context in each of those multi-step scenarios.

**1:02:40** · So we are not just limited by task duration.

**1:02:42** · How well we do in terms of quality of synthesis at these time horizons also has a lot of headroom for improvement.

**1:02:53** · And, how does this vary from a real world task?

**1:02:56** · So, I mean, as I said before.

**1:02:58** · So benchmarks are never perfect.

**1:02:59** · They are a representation of what we think is measurable today.

**1:03:04** · And so METR is automatically scored.

**1:03:07** · There's no multi-agent interaction.

**1:03:09** · So it's basically targeting a set of tasks that are single agent.

**1:03:15** · And it's not punishing of mistakes.

**1:03:16** · And the resource constraints, there is no resource constraints in terms of how much resources can be used.

**1:03:22** · So it's basically, in real-world, you might actually have more subjective constraints in how things are scored.

**1:03:30** · You might be able to break down the task into multiple agents, which might actually lead to a better evaluation.

**1:03:36** · And then there might be actual resource constraints or cost of mistakes.

**1:03:42** · In the second set of paper that we covered called GDPVal, which focuses very much on economically valuable tasks, the key aspect there is that the tasks are extremely well specified, all the contexts that the human would have in their head gets specified in the task.

**1:03:57** · And it's one shot.

**1:03:58** · So there is no iterative back and forth where you get to fix what the model did.

**1:04:03** · And it requires the model to have some amount of tacit knowledge.

**1:04:07** · So it needs the knowledge to be there already in the model.

**1:04:11** · And that gap gets covered more by the third benchmark that we were looking at research synthesis.

**1:04:16** · Here the challenges are that the models still struggle with finding comprehensive, high-quality sources and surfacing key facts and then verifying them.

**1:04:26** · And these are things that, if a human is an expert in the field and does this day in and day out, they'll be much faster at because they just have that context in their head all the time.

**1:04:37** · So, what do we know now in terms of model capabilities and where there's headroom for improvement?

**1:04:42** · So we kind of know that the models have been improving on isolated, well-specified tasks.

**1:04:47** · If you have a set of tasks that are well-specified and fall in the set of domains where the models are good at, then they do a really good job.

**1:04:55** · Software engineering and ML research are two domains where we have seen significant progress, perhaps because as computer scientists and computer engineers, we tend to understand those domains better.

**1:05:05** · So we are automating away our own jobs.

**1:05:09** · So we definitely are seeing these models do a really good job in terms of solving hour long tasks there.

**1:05:17** · And the stronger models can generate very well organized outputs, even if not all parts of that outputs are correct.

**1:05:25** · What we have lower confidence in, if you look at model capabilities, is that the model's performance on tasks where you need a lot of context is low.

**1:05:35** · So if you don't have the context in the model's prompt, then the model doesn't quite know what to go work on.

**1:05:41** · It doesn't quite figure out ambiguous prompts, and just figure out what it needs to figure out to solve the problem.

**1:05:50** · The performance in adversarial environments is not necessarily great.

**1:05:55** · Overall, if you want 95% reliability, the models are not quite there.

**1:06:00** · And generally, we have not yet seen a lot of generalization beyond software and knowledge work.

**1:06:05** · Knowledge work encompasses a lot of the digital workloads today.

**1:06:12** · We also think that the models are still not strong at finding comprehensive, high quality sources when they have to reference knowledge bases and surface key facts, and then verify what they surfaced as high accuracy and high coverage in the knowledge base.

**1:06:29** · So all of these are still gap areas in model capabilities.

**1:06:34** · So if we were to summarize across the three papers that we talked about today, in METR, we talked about the seven-month doubling horizon in terms of model capabilities.

**1:06:46** · As in the models can complete the tasks with 50% reliability.

**1:06:52** · That time horizon has been doubling every seven months.

**1:06:55** · And the forecast is that say, 2028 to 2031, it will almost be a one month.

**1:07:01** · Task can be completed by the model.

**1:07:05** · But that view gets contradicted in some ways by GDPVal win rate, which shows more of a linear improvement over the last two years, where even though the win rate for a certain set of tasks is 48%, at the same time, you will see that there are many category of tasks that don't have high win rates.

**1:07:23** · And then the other gap area that you see is that a lot of the tasks in GDPVal actually require context or require looking at reference data.

**1:07:30** · And DeepScholar-Bench, the research synthesis task kind of shows you that there are critical gaps when you have to go retrieve some set of context or look at a knowledge base.

**1:07:39** · And generally, the quality and the verifiability don't quite match up compared to what a human would be able to do.

**1:07:48** · So in general, the reliability and the error recovery of the model should continue to improve, but the performance will vary still over task types, like which category of tasks we are looking at.

**1:08:00** · So even if the models are solving longer and longer horizon tasks, that doesn't necessarily mean they're always giving highly reliable or quality outputs.

**1:08:08** · So we need metrics which are duration-based, economic value-based, and also synthesis quality-based.

**1:08:14** · And you still need to validate them against humans who can solve these tasks.

**1:08:20** · OK with that, I will actually open up for questions.

**1:08:27** · If you go back to the first task for the \[INAUDIBLE\] team.

**1:08:31** · So what do you think about the \[INAUDIBLE\] it's similar to many like Moore's law.

**1:08:43** · So I'm just curious because you are much experts than me.

**1:08:47** · What do you think \[INAUDIBLE\]?

**1:08:50** · So I think there's two answers to your question.

**1:08:52** · I mean, SWE-bench definitely shows-- SWE-bench Verified, for example, has shown a really strong growth.

**1:08:58** · In general encoding area, we will continue to see improvements.

**1:09:03** · And still there is a large category of tasks which are not just pull request-based and so on.

**1:09:11** · And these are hard tasks.

**1:09:12** · So there's a long path that will continue to be challenging for the longest.

**1:09:18** · I mean, Waymo, the first \[INAUDIBLE\] easy to do, and then the last 20% \[INAUDIBLE\].

**1:09:28** · Distributed systems being one of the areas in which computer science, where it's very hard for the model to get it right.

**1:09:38** · You've mentioned a couple times automating \[INAUDIBLE\].

**1:09:44** · What is your sense of how you expect your own work to look different two years from now?

**1:09:57** · So I think AI timelines are moving extremely fast in ways where it's very hard to predict something one year from now.

**1:10:06** · I think one of my tasks would end up being \[INAUDIBLE\] what an AI scientist does, and AI scientists being able to come up with hypotheses and run experiments and then complete the whole loop is still something of-- that is our definition of AGI is to when AI can build the next generation of models themselves, then we don't have to even be in the loop.

**1:10:29** · But I don't think that is quite there yet.

**1:10:32** · But it's definitely been fascinating to see the level of progress in terms of how the AI models do have the knowledge base and often are extremely strong brainstorming partners.

**1:10:44** · So as AI co-scientist at this point in time, which has a better value for a lot of the use cases, is what I see.

**1:10:57** · I also generally feel that in most areas, getting reliability or the long tail of reliability is going to be extremely challenging.

**1:11:06** · So that's the area in which the last mile is hard to get progress on.

**1:11:16** · I thought more of a clarification question about the beta paper.

**1:11:21** · So they talk about this concept of 50% pass completion rate.

**1:11:26** · I was wondering if the 50% is like an average success rate, maybe, let's say, let's say they're like 100 test instances.

**1:11:36** · And then for each test instance, AI will try 10 times.

**1:11:39** · And then you see you count how many times that it fails or succeeds.

**1:11:43** · And then you take the average over the 100 times 10, or is it more like you want to be make sure for every task, it has at least 50% because I feel like the latter would be much more stringent and harder to achieve.

**1:11:58** · I think it's multiple attempts for sure, because if you remember, we showed this plot.

**1:12:02** · So there are multiple agent runs and it's basically saying how many times it completed successfully.

**1:12:09** · So you have maybe-- so, yeah, so here let's say there are 97 tasks.

**1:12:13** · So each task, you would calculate a success rate of the agent.

**1:12:18** · And then you take the average of the individual task success rate across the 97, is that what you think they're doing to get the final 50%?

**1:12:29** · So yes, roughly, right?

**1:12:32** · For each horizon, they're basically drawing these points.

**1:12:36** · And the points are-- the success rate for each task is coming from what percentage of attempts were successful.

**1:12:46** · So 50% success rate for a particular task roughly would mean that 50% of the time, it might come back with a good answer, 30% maybe not.

**1:12:54** · So it's a flip of a coin.

**1:13:07** · \[INAUDIBLE\] so AI is doing much better.

**1:13:13** · So it's \[INAUDIBLE\] engineering job \[INAUDIBLE\].

**1:13:20** · OK, let's take that off for the class.

**1:13:25** · I think the computer science as a profession is not going anywhere.

**1:13:29** · And if you are able to reason for fundamentals, that is a very important skill to have.

**1:13:35** · AI, as you saw, needs to figure out the context or solve anything.

**1:13:39** · So you need to be able to give it the context.

**1:13:43** · So that's my belief.

**1:13:52** · All right, I have a question.

**1:13:54** · What do you think are stopping AI from tackling those long tail problems?

**1:14:01** · Is it lack of data?

**1:14:03** · Or what else, I mean, what's the fundamental limitations?

**1:14:09** · It's a mix of both a data problem and a fundamental model capabilities.

**1:14:13** · In certain cases, if you-- I think there are several startups that are tackling things and building environments and whatnot, but coming up with tasks that are representative and then stopgap in the model capabilities in each of these tasks continues to be an area which is challenging at this point in time.

**1:14:32** · So I think when they are broad across categories like, say, legal research or financial research, those have seen much faster adoption and improvements.

**1:14:43** · But when they're very, very specific, like having enough data to or having the model progress in the right model capabilities is hard.

**1:14:52** · For example, if you look at robotics as a domain, which is the embodied AI stuff, there's a whole suite of startups that are just going after data collection as the primary hypothesis to close the gap based on top of these models.

**1:15:08** · OK.

**1:15:10** · Thank you.
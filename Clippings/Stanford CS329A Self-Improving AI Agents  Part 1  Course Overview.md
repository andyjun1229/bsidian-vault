---
title: "Stanford CS329A Self-Improving AI Agents | Part 1 | Course Overview"
source: "https://www.youtube.com/watch?v=6YnLB0XbTnI&list=PLangBM27OtEA&index=1"
author:
  - "[[Stanford Online]]"
published: 2026-08-03
created: 2026-08-26
description: "Want to dive deeper? This curriculum is covered in the following online courses:- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html- XCS329 graduate course:"
tags:
  - "clippings"
---
?![](https://www.youtube.com/watch?v=6YnLB0XbTnI)

Want to dive deeper? This curriculum is covered in the following online courses:  
\- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html  
\- XCS329 graduate course: https://online.stanford.edu/courses/cs329a-self-improving-ai-agents  
  
A similar curriculum is covered in XCS329z https://online.stanford.edu/courses/cs329z-engineering-ai-agents  
  
Follow along with the course schedule and syllabus: https://cs329a.stanford.edu/  
  
View the course playlist: https://www.youtube.com/playlist?list=PLangBM27OtEA  
  
Video Summary:  
This first lecture videoof Stanford's CS329A, Self-Improving AI Agents, taught by Aakanksha Chowdhery and Azalia Mirhoseini on September 22, 2025, opens with an overview of scaling laws that link model parameters, training compute, and dataset size to lower test loss in large language models from GPT-2 through GPT-4. It covers few-shot and zero-shot learning, the emergence of chain-of-thought reasoning in larger models, and the role of instruction tuning and reinforcement learning from human feedback in the development of ChatGPT. The lecture introduces inference-time scaling through the Large Language Monkeys project, which repeatedly samples a model's outputs and selects correct answers with a verifier to improve performance without retraining. It then traces the shift from single-turn chatbots to agent workflows such as prompt chaining, routing, parallelization, and orchestrator-worker patterns, using Claude Code and deep research tools as examples. The session closes with logistics for the course.  
  
Speaker Bios:  
Aakanksha Chowdhery  
Adjunct Professor of Computer Science, Stanford University  
  
Dr. Aakanksha Chowdhery is pushing the frontier of agentic LLMs, focusing on recursive self-improvement and long-horizon agents that learn and deploy in the real world. She is one of the few researchers globally who has led frontier model training end-to-end, across both dense and mixture-of-experts (MoE) architectures. At Google, she led the 540B PaLM model, the largest densely trained language model in the world at the time. She subsequently drove pre-training and scaling of Gemini's MoE models across multiple generations, and contributed key components to PaLM-E, Med-PaLM, and the Pathways infrastructure underpinning Google's large-model efforts. She went on to build and lead pretraining teams for open intelligence efforts at Reflection and Meta. Earlier, she held research roles at Microsoft Research and Princeton. At Stanford, where she earned her PhD, she teaches CS329A (Self-Improving AI Agents) and serves as Program Chair for MLSys 2026.  
  
Azalia Mirhoseini  
Assistant Professor of Computer Science, Stanford University  
  
Azalia Mirhoseini is a co-founder of Ricursive Intelligence, a frontier lab dedicated to recursive self-improvement through AI that designs the chips that fuel it. She is also an Assistant Professor of Computer Science at Stanford University where she directs Scaling Intelligence, a lab focused on developing scalable and self-improving AI systems and methodologies toward the goal of artificial general intelligence. Previously, she spent several years in industry AI labs, including Google Brain, Anthropic, and Google DeepMind, working on the development of Claude and Gemini. Her past work includes Mixture-of-Experts (MoE) neural architectures, now predominantly used in leading generative AI models; AlphaChip, a pioneering work on deep reinforcement learning for layout optimization used in the design of advanced chips like Google AI accelerators (TPUs) and data center CPUs; as well as pioneering research on LLM Test-Time Scaling. Her work has been recognized through the Okawa Research Grant, the Google ML and Systems Junior Faculty Award, MIT Technology Review's 35 Under 35 Award, the Best ECE Thesis Award at Rice University, publications in flagship venues such as Nature, and coverage by various media outlets, including WSJ, NYT, Forbes, MIT Technology Review, IEEE Spectrum, WIRED, and TechCrunch.

## Transcript

**0:05** · Welcome, everyone, to fall quarter and welcome to CS329A.

**0:10** · I hope you made it to the right class.

**0:11** · This class is on self-improving AI agents.

**0:15** · Anyone made it to the right class here?

**0:18** · Yes.

**0:20** · Yes?

**0:21** · OK.

**0:22** · How many of you are here and doing masters at Stanford?

**0:27** · OK.

**0:28** · PhD?

**0:30** · OK.

**0:31** · Few of you.

**0:31** · And then undergrad?

**0:34** · OK.

**0:35** · So masters is the big crowd here.

**0:37** · There's a good balance.

**0:39** · It's a really good balance.

**0:41** · So we'll introduce ourselves.

**0:43** · So I'm Akansha.

**0:44** · I have been working in large language models for a while, and I'm an adjunct professor at Stanford.

**0:48** · And I'm also in research at a startup called Reflection AI.

**0:52** · Hi, I'm Azalia Mirhoseini I'm.

**0:56** · An assistant professor in the CS Department.

**0:59** · And Akanksha and I met each other when we were at Google Brain.

**1:07** · Google Brain.

**1:07** · Yeah, back in the day.

**1:09** · And then Google DeepMind.

**1:10** · And I also worked on Claude and Anthropic and Gemini at Google DeepMind.

**1:16** · And we are so excited to teach this course again.

**1:20** · This is the second time we're teaching.

**1:21** · Of course, we have made some updates, both to the lectures and also the way we are conducting everything for the course.

**1:32** · And we were just so amazed by the amount of interest for people to join this course.

**1:38** · So we are excited to have you here.

**1:41** · The course website is at cs239a.stanford.edu.

**1:45** · We have updated the website in terms of all the lecture materials and the papers that you'll be reading, as well as what's the homework schedule to expect the project proposal and project structures as well.

**1:58** · So in today's lecture, we'll start with an overview of large language models, just how the scaling trends have evolved over the last five years.

**2:07** · And then we'll focus more on what we will cover in this class.

**2:10** · And then from there, in the second half of this lecture, we'll cover the course logistics.

**2:16** · And that part, you should pay a lot of attention to, because that influences your grades.

**2:23** · So let's take a look at an overview of the trends for large language models.

**2:27** · So one of the aspects that has been mind blowing since GPT 3 came out is that as you scale up the number of parameters in a model, they get better.

**2:40** · And what this means is that language models like Bert and T5 were good.

**2:45** · But as we increase the number of parameters, they got really better.

**2:48** · They perform much better.

**2:50** · And what this led to is something called a scaling loss for large language models, which are used in building the base model for-- the pre-trained base model.

**2:59** · And as you increase the amount of compute-- so there are three graphs here.

**3:03** · As you increase the amount of compute on the x-axis, the loss function on the y-axis goes down.

**3:09** · And the more compute you have put in, the more the test loss goes down, which leads to a better model.

**3:16** · So that was one big aspect that led to GPT 3, then all the subsequent-- ChatGPT, PaLM, Gemini, and so on.

**3:25** · And then similarly, as you increase the data set size on x-axis, the test loss goes down further on the y-axis.

**3:32** · So that's another aspect of-- another axis of scaling that leads to better language models.

**3:38** · And the third one is, of course parameter counts.

**3:42** · So if you increase the number of layers in a transformer or the amount of parameters that are there in the language model, that improves the loss value, and that leads to a better model.

**3:52** · And this has been the foundation for a lot of-- this has been the foundation for a long time, until last year, where this was starting to hit some kind of a saturation point.

**4:04** · So from 2018 to almost 2024-- this graph is a little bit outdated.

**4:10** · But from 2018 to 2024, as the model size has gone up almost consistently, we have been increasing the size of the model.

**4:19** · So you started with something like Bert was 340 million parameters, GPT 2 was 1.5 billion parameters, and then GPT 3 was 175 billion parameters, and then PaLM was 540 billion.

**4:31** · And then there was a bunch of subsequent models.

**4:34** · And GPT 4 is estimated to be there, which is trillions of parameters.

**4:38** · So you can imagine that there has been an exponential growth in just the model size for large language models.

**4:44** · The large stands for that they're growing in size.

**4:47** · And that has been one of the key areas in which the models have been getting better.

**4:53** · So why do we care about the models getting bigger?

**4:56** · What does this lead to?

**4:58** · So as I was explaining that as the models get bigger, they continuously improve in performance on natural language benchmarks on various other benchmarks, reasoning benchmarks, and so on.

**5:08** · And then the other interesting aspect that I will show you in a moment is that they learn how to do few shot learning.

**5:15** · So earlier, you have to fine tune the model for specific domain.

**5:18** · But just by giving a few examples, the model can follow that template and reason in that same vein, which makes it extremely easy to prototype things.

**5:29** · And then the third aspect is that as the models become bigger, they have emergent behavior where the capabilities like reasoning only emerge in larger models.

**5:39** · So just to understand few shot learning or zero shot learning here.

**5:43** · So if the model is given a question or a task, like translate English to French, it's able to give-- so this is called a prompt.

**5:52** · Like it's a given a task, translate English to French.

**5:55** · And then it's asked to translate cheese to whatever is the French word.

**5:58** · If the model can predict the answer without actually being trained on the specific task, then that would be called zero shot learning.

**6:05** · And then few shot learning, in addition to giving the description of the task, you're also giving a few examples.

**6:12** · So in this particular case, it's giving, translate English to French.

**6:15** · And it's given a few examples of the translation from English to French.

**6:19** · And then it's asked to translate cheese and it's able to translate that.

**6:22** · And you can see that this capability shows up in the large language models across a large number of tasks.

**6:28** · And that has been one of the key areas that GPT 3, PaLM, and other models enabled.

**6:33** · And then that subsequent innovations came from reasoning aspects of this.

**6:39** · So on the reasoning side, as models have become bigger, they have this emergent behavior of reasoning, which Azalia will tell us a little bit more about.

**6:48** · So as the models become bigger, not only we have this predictive scaling laws property that we know how the loss function is going to go down as we throw in more compute data and parameters in the model, there are new behaviors that appear in the model that they didn't have before.

**7:09** · And we never could predict that until we had these bigger models and saw this behavior in them.

**7:14** · And one of the most important-- one of those behaviors is the chain of thought behavior.

**7:23** · And for those of you who are not familiar with this, here is how it works.

**7:28** · So in a usual prompting of a model, we can ask a model, in this case, a math problem.

**7:36** · And then we can give it a one shot example.

**7:39** · Here is a math problem, here is the answer.

**7:41** · Now I ask you a similar but not exactly the same math problem.

**7:47** · And the model is expected to answer that.

**7:51** · And the model might be able to use the one shot example, or it might not be.

**7:55** · But we can do better here by not only give an example, but also provide the reasoning or the chain of thought on how we got to that answer.

**8:06** · So in this case, the question is a very simple question.

**8:10** · Roger has five tennis balls.

**8:12** · He buys two more cans of tennis balls.

**8:16** · Each can has three tennis balls.

**8:18** · How many total tennis balls does he have now?

**8:21** · And instead of just saying 11, you're walking the model through how to get to this.

**8:27** · Roger started with five balls.

**8:28** · Two cans of three tennis balls is 6, and 5 plus 6 is 11.

**8:34** · And with this example, then the model has become familiar with the process to get to the answer.

**8:41** · And it can leverage that to answer new problems.

**8:46** · Well, obviously, this is a very simple problem.

**8:49** · Any 1B parameter model nowadays can solve this.

**8:52** · Doesn't need an example or a few shot or a chain of thought.

**8:56** · But the chain of thought property itself is a property that is holding to this day.

**9:01** · And it's a very, very important property for the reasoning models and all the thinking models and much of the progress that we have seen in the past year or so.

**9:14** · Now, this property again appears as we have larger and larger models.

**9:20** · Here are three models, LaMDA, GPT, and PaLM.

**9:24** · And as you can see, the chain of thought.

**9:26** · And this is some results on some math data set.

**9:30** · And these models, when they're smaller, like eight billion parameter for LaMDA, or for GPT, around 7 billion, they can't really benefit from chain of thought.

**9:42** · It doesn't do anything for them.

**9:44** · But as they become larger or for a pull mother again at 8 billion, it can leverage this chain of thought property and learn from the reasoning and the process that is provided in the context in order to solve problems better.

**10:03** · And not only that, there are other abilities to solve new tasks as we increase the size of the models.

**10:10** · Like, for examples, models can all of a sudden solve mod arithmetics better or solve word unscrambled problem just by having this larger size and this property.

**10:23** · You see that all of a sudden, it appears at a certain size.

**10:27** · And because of all of this, we still, as in frontier companies and labs, are still interested in pushing the scaling laws and not only get the natural kind of progression, but also we will see more and more of these emergent behavior that is going to be very important.

**10:49** · Now, a little bit of history here.

**10:52** · So ChatGPT was launched in November 2022.

**10:58** · Obviously, it was one of the most successful apps or software ever created.

**11:05** · The time to reach one million users for it was five days, which is significantly faster than many of the other famous software that you can see there, or services that you can see there.

**11:20** · And there were pieces of innovation on top of just scaling up the parameter size of the model that were very important to make ChatGPT what it was and to make that leapfrog over the previous models, like GPT-3, so on.

**11:39** · And two important pieces here were the instruction tooling and the reinforcement learning from human feedback, which we are going to briefly mention in the next slides.

**11:52** · But throughout this course, we are going to learn more and more about them.

**12:01** · And then we're going to learn about all of these in more details.

**12:05** · But let's just take a step back and see how the process works.

**12:09** · So the pre-training step is the step at the beginning of any language model training.

**12:17** · That's the easiest step.

**12:19** · And we just train the model to predict the next token out of all sorts of text and data, and so on.

**12:25** · And then this is the fine tuning step that was a key differentiating factor for a model like ChatGPT.

**12:33** · And let's start with the first aspect of fine tuning, which is alignment with human preferences.

**12:43** · So when a model is pre-trained, it has no sense.

**12:47** · It has seen all data on the internet, in the books, everywhere.

**12:51** · But it has no sense of what is right and wrong and what is.

**12:55** · It just statistically knows about the state of the worl, but does it doesn't exactly know things or know how to follow instructions.

**13:03** · So the next step in training these models is the step where we try to steer the AI models to follow the goals and preferences and values of humans.

**13:18** · And this is still a big problem.

**13:20** · It's a big issue.

**13:21** · We haven't mastered it yet.

**13:24** · But as we progress, models are becoming better and much more powerful in the things that they can do.

**13:35** · So it turns out that we can fine tune the models to be aligned.

**13:39** · For example, here are some graphs that show, what if we take our base model that's just pre-trained and fine tune it for things like sensibleness or safety?

**13:51** · And these are data that we have collected.

**13:56** · These are high quality data for showing the model what we mean by what's safe and what's unsafe or what's sensible and what doesn't make sense.

**14:05** · And these are more curated, more highly curated data that we pass to the model for fine tuning and to make the model more aligned with the values or the preferences of humans.

**14:21** · So going back, let's just walk through this process again.

**14:26** · So the first stop when we take a pre-trained language model is fine tuning with next token prediction, which follows the same process as pre-training.

**14:39** · But this time on data that is much more higher quality.

**14:44** · For example, this could be data from books, creative essays.

**14:50** · Data that companies pay a whole lot, millions of dollars or hundreds of millions of dollars potentially, to buy this data that's really high quality.

**14:58** · And then we train them.

**14:59** · We fine tune the model on those, and the model becomes much better as a result of that.

**15:07** · The next step is instruction tuning.

**15:11** · And by instruction tuning, what we mean is that we show the model.

**15:15** · Again, traditionally in the past two years, this instruction tuning data is a combination of human generated data role templates and the synthetic data.

**15:28** · But the way this instruction fine tuning works is that we do have instruction and then question answer pairs, where the model learns how to follow the questions and answers them.

**15:41** · For example, here, an instruction tuning data set could be about the weather.

**15:48** · Please answer the following question, what is the boiling point of nitrogen?

**15:52** · And then this is the answer.

**15:55** · Or we can have chain of thought fine tuning, where we show the model how it can walk through a process to get to the answer.

**16:03** · And then we have the label.

**16:05** · We have the result over here.

**16:07** · And this is like these pairs of questions and instructions and answers.

**16:11** · And again, this data set is very-- there's a lot of effort that goes into this data set.

**16:19** · And the quality of data set and the generality of it has a lot of impact on the quality of the model that we get at this stage.

**16:28** · And after this point, then the model becomes more and more like the models we see today.

**16:35** · You can ask them questions, you can go back and forth with them.

**16:39** · They have this sense of how to perceive a question and how to walk through some process to get to an answer.

**16:51** · And the next step after instruction fine tuning is this process of using human preferences and fine tuning the model based on that.

**17:01** · And this process is called RLHF, or Reinforcement Learning from Human Feedback.

**17:08** · The way this is different from the previous step is the way we create the objective function and create the data.

**17:15** · So in this case, instead of just creating some supervised prompt and labels, we are basically creating a reward model out of human preferences.

**17:27** · So companies spend a lot of money asking humans, sometimes experts, sometimes just humans, normal humans, about questions and the answers generated by the model.

**17:41** · And we asked the humans to rate them, to see which one is correct, and which one is not correct, and that's how we can create some sort of a reward model here.

**17:52** · And this reward model is instead of human.

**17:55** · Then we can use the reward model in order to guide the parameters of our LLM towards generating answers that are in line with this reward model.

**18:06** · So basically we want the generations by the model to be such that this reward model says yes, these are good generations.

**18:14** · We're going to learn more about this here, but we wanted you to have the high level idea of what RLHF means.

**18:24** · We can have different reward types, different types of reward.

**18:27** · For example, we could ask the model to reward a pair of answers based on their correctness or helpfulness or specificity or harmlessness.

**18:36** · All reward functions that we can define.

**18:38** · And depending on how we want the models to be and what we care most about, we can weigh these different reward models and use that in the RLHF process.

**18:50** · So these step at a high level, of course, there's a lot of effort goes into that.

**18:55** · But pre-training and then fine tuning on higher quality data instruction tuning and RLHF were the core components that made up a model like ChatGPT over something that existed, over all the large models like GPT-3 and prior models.

**19:18** · So that made a huge difference in how good and capable the models were.

**19:25** · So that was very cool up until last year.

**19:29** · Or a year and a half ago.

**19:32** · Pre-training and then fine tuning were the big pieces.

**19:35** · But since a year and a half ago, it turns out inference is also a frontier for making the models much more capable.

**19:45** · So and that opened a whole set of whole lot of new research and directions and ways that we can make the model better.

**19:55** · So let's talk about it a little bit.

**19:59** · Like this is the work we did in my lab last year.

**20:03** · Last summer, and it was called Large Language Monkeys.

**20:08** · And it's inspired by the infinite monkey theorem.

**20:11** · And it's related to inference scaling.

**20:14** · How many of you have heard of the infinite monkey theorem?

**20:18** · OK, that's a good amount.

**20:20** · So the idea of the infinite monkey theorem, what it says is that it's not proven.

**20:26** · But what it says is that if you have a monkey and a typing machine, and then we keep letting the monkey type all day forever, after some time, we will have the works of William Shakespeare in the things that the monkey types.

**20:43** · So we were inspired by that to name our project.

**20:46** · But the idea here was that, let's have the LLM be the monkey.

**20:52** · And let's ask the model over and over again to solve a given input problem.

**21:01** · You can think of it as parallel sampling or parallel generation.

**21:05** · So instead of asking the model once to solve the input problem, you can ask it many times.

**21:10** · And also, let's assume you have some sort of verifier or selection mechanism so you can pick which one of these generated responses were correct.

**21:21** · And then you output that in your system.

**21:23** · That becomes the final output.

**21:26** · So the model, instead of generating one answer, generates many, many answers.

**21:30** · And then your verifier selects which one of them is correct and then outputs one of the correct ones.

**21:36** · You can think of a verifier as, say, some unit tests.

**21:40** · If the problem is generating code, the verifier could be the unit test that we run against the code, and we see which one of the code generation passes all the unit tests, and so on.

**21:53** · The reason this can be a possibility here is that models are not-- there is some variance in the way the models generate responses.

**22:07** · It's not deterministic.

**22:08** · And you can even control the variation in the model responses with this thing called temperature.

**22:13** · So you can force the model or encourage the model to generate more different responses as you ask a question.

**22:23** · And here, now let's see some of the results of this repeated sampling.

**22:29** · For a bunch of tasks, like math and coding benchmarks, we increased the number of samples per problem from 1, which is the normal one, to 10,000.

**22:43** · And here, we are showing the coverage or the fraction of problems that are solved by at least one of these samples.

**22:50** · And what we are seeing here is that so the red line, the red dashed line, was the GPT-4o model.

**22:59** · And while these blue and green lines, which were the normal HP, the normal 3HP and 7AB, were worse than GPT-4o model with one sample.

**23:10** · But if we increase the number of samples from these models, in all of these cases, they do better than the GPT-4o model.

**23:21** · And what it says is that it kind of seems like the models already know a whole lot more than what you get out of them when you just ask them once, right.

**23:33** · So this is the underlying property of inference scaling, because it seems like we can get a whole lot more capability and problem solving ability from these models if we just bring in this inference scaling.

**23:49** · Here, we are showing repeated sampling, but there are many other ways to do that.

**23:54** · So the reason it's called inference scaling is that we are not touching any of the parameters of the model.

**24:00** · The model is fixed, and we are just at inference time.

**24:03** · We are creating different ways to generate, to produce generations from the model and use them to generate higher quality answers or answers to harder problems for the model.

**24:15** · The interesting part here is that for some of these problems, out of these 10,000 solutions, maybe three or four of them were correct for a single problem.

**24:26** · So it shows that how important it is to scale the inference to really get to the core capability of the models.

**24:38** · But what is the difference of ways of traversing all of the possible answers and just \[INAUDIBLE\]?

**24:56** · Sorry, what's the question?

**24:57** · What is the difference of just ways of traversing all the possible answers and \[INAUDIBLE\]?

**25:04** · So the possible answers need to be generated somehow by the model, right?

**25:11** · So the space of all possible answers to the model is way bigger.

**25:18** · if we do like a tree search or a random search, it's way bigger, right.

**25:22** · There's no way to hit.

**25:23** · Even imagine we are asking a human, just sit down and solve this problem, right.

**25:33** · Of course, there's no limit to human creativity, human's creativity.

**25:37** · But there is a limit to how many generations we can have, right.

**25:40** · Or if we randomize things, there's a whole lot set of answers that can be generated.

**25:46** · And this is highly sample efficient, right.

**25:50** · 10,000 is not a whole lot.

**25:51** · Especially like, for example, for the math f to f.

**25:56** · Some of these problems are really hard IMO level problems.

**26:00** · These are really hard problems that a tiny model like a 7 and Llama ATP can solve.

**26:07** · I was thinking, how does the latency compare to when you do actually generate all those samples compared to the GPT-4o, right?

**26:18** · How does the latency-- is tradeoff for you?

**26:21** · Yeah, of course, there's a tradeoff.

**26:24** · And we touch on that in the lecture that I go more details towards this.

**26:29** · The parallel samples, the good thing about them that they can be run in parallel.

**26:34** · So from a latency perspective, that's less of an issue.

**26:37** · But of course, there is the frontier of cost tradeoffs between how much compute you're spending.

**26:43** · And we will look into that.

**26:44** · And it varies.

**26:45** · It varies depending on the type of and complexity of the problems.

**26:50** · Yes?

**26:51** · This approach where you have a verifiable domain like math and coding and how do you handle it when you don't have-- Yes, great question again.

**27:02** · When you have verifiers, it's much easier.

**27:04** · When you don't have verifiers, there's this whole set of research on how to train LLM as Judge or LLMs reward functions or LLMs with tools becoming.

**27:14** · And we're going to learn about that all.

**27:16** · We have a lecture just dedicated to verifiers, so.

**27:22** · Yeah?

**27:22** · Just a quick question, sorry.

**27:23** · So does this generalize to any positive temperature?

**27:29** · So as the limit, as the temperature goes to infinity-- No.

**27:37** · Yeah, we can have the temperature being too high, because it's going to be gibberish.

**27:41** · The model doesn't generate.

**27:43** · So there's actually a research project last year was on tuning that or figuring out what temperature.

**27:51** · Usually if you go beyond 1.2 or so, it's not great, yeah.

**27:57** · Yeah.

**27:58** · But there are other tricks that you can do to make the model be more-- have more diversity in the type of answers.

**28:09** · And that can be useful.

**28:12** · All right.

**28:16** · So let's look at this.

**28:20** · So now, again, going back to the events of last year, year and a half, we had the DeepSeek model.

**28:28** · I think it came out in December.

**28:31** · Christmas.

**28:32** · DeepSeek came out December 2024.

**28:36** · Oh, wow.

**28:37** · It's been a short time.

**28:38** · Short time or long time, I don't know.

**28:42** · So then models like DeepSeek came last year.

**28:46** · So basically, a core innovation in DeepSeek.

**28:49** · And then the one series Gemini thinking and such were that.

**28:53** · Now we are bringing this fine tuning and test time scaling together.

**28:58** · Because with this test time scaling and the models themselves, we have this new engine that we can generate a whole lot of synthetic data.

**29:09** · For example, for problems like for math problems, where we know the answer.

**29:13** · We can have the model generate different answers that leads to that final golden answer.

**29:21** · Or for the coding problems, we can use the model to generate tons of data during test time scaling, tons of quality data to solve coding problems.

**29:31** · And that becomes part of our training set.

**29:33** · Now we can use that to fine tune the model to become better.

**29:38** · So that, bringing these two together became a big piece in thinking models and reasoning models.

**29:46** · And this is an area that is really, really important.

**29:52** · There's just so much to be explored in this.

**29:54** · Because again, it's open-ended, right.

**29:58** · There's no boundary in how good the models can become with test time scaling, and then bringing that back to the process of training the model or fine tuning the model to become better is very exciting.

**30:10** · And that's the self-improving piece that we are very excited about.

**30:17** · So a little bit about reasoning models.

**30:20** · In the language monkeys, what we were showing was the coverage.

**30:23** · If we had access to verifiers, we can see the log linear scaling laws with the number of samples.

**30:32** · And OpenAI, when they released o1 last September, they showed the log linear relationship, this time with pass at one for these hard aiming benchmark, which is a set of really difficult math questions.

**30:51** · So what they're showing here is that as they're increasing test time compute, and this is in log scale, the accuracy, the past one accuracy of the model goes up.

**31:05** · And this is for test time alone.

**31:07** · Previously, this has been shown for training, but it's very interesting that this kind of scaling applies to test time as well, without changing the parameter count of the model.

**31:22** · I'm going to walk you through a few examples of how this reasoning or test time scaling works with models like O3 or Gemini.

**31:35** · So one motivation here is that for difficult problems, just like humans, think a lot more, spend a lot more time, or consider many different strategies, thinking models do the same.

**31:48** · And they may use a chain of thought or other techniques to just go about solving a problem.

**31:57** · And there are different steps to that.

**32:00** · For example, problem analysis is one step.

**32:04** · The model first sees a problem and tries to analyze it.

**32:08** · Then it can do the task decomposition.

**32:11** · Breaking a task into simpler tasks that are more addressable.

**32:16** · Then there is the self-evolution strategies where the model tries something, sees the feedback.

**32:24** · For example, runs some tests on the code or uses a calculator, or just judges the answer.

**32:32** · And it can use that feedback to optimize itself.

**32:36** · There's self-correction, and there are alternative proposals.

**32:39** · If something doesn't work, the model can backtrack and try a different approach.

**32:46** · These are some key principles that the model probably at some point, pieces of it were trained as part of the training data set were curated by humans.

**32:58** · But a big part of it is also the model acquiring these skills during this fine tuning process and RL from synthetic data process that the model does.

**33:11** · Here is an example of how o1 does analysis.

**33:17** · The model is asked to write a bash script that takes a matrix and then outputs the transpose of that matrix.

**33:26** · And the model starts with, just like humans, starts thinking, what are the pieces, important pieces, here?

**33:34** · So the user is requesting a bash script.

**33:37** · Let's understand the input and output formats of this matrix, and so on.

**33:44** · So the model just thinks itself.

**33:47** · And amazingly, it's like a progression of chain of thought.

**33:52** · This is like helping the model finding the answer.

**33:55** · But the difference between chain of thought and this is that the model itself is producing this chain of thought.

**34:02** · There's, of course, task decomposition, in this case, for the approach.

**34:09** · The model thinks about parsing the input, building the matrix as an array of arrays and so on.

**34:17** · There's also self-correction, which is a big important piece of-- this is an important piece here.

**34:23** · And I don't know how many of you have seen that when trying with the models that you can see the thinking traces.

**34:30** · And this is actually pretty common.

**34:31** · The models start something, and then in the middle says, wait, the correct-- there's something wrong, maybe.

**34:39** · And maybe I need to fix that.

**34:41** · And it's very, very cool that the model can do that itself.

**34:45** · So reasoning models, when they came out, like models like o1, compared to a model like GPT-4o, which wasn't a reasoning model, they tend to be better in obviously the reasoning task.

**34:58** · For example, in math calculation, data analysis, programming and such, they all outperform GPT-4o, but not necessarily in personal writing or editing texts, and so on.

**35:12** · Yeah, question?

**35:16** · Do you think the gains due to this asking for a reasonable price is due to actually the act of generating this reasoning traits, or just the act of asking the model to think or do these decomposition at all?

**35:29** · Like, for example, if you said, think step by step, but don't generate out loud, but actually generate false positive \[INAUDIBLE\] without saying.

**35:39** · Yeah.

**35:41** · I repeat the question.

**35:43** · You were saying, do you think the reasoning models are becoming what they are?

**35:49** · Is it based on the loud way of thinking?

**35:53** · I think the question is that, is it because of the reasoning, or is it because of things step by step, the chain of thought?

**36:01** · Is it the data that's making a difference, or is it the instruction?

**36:05** · I mean, so the data basically has made the model become a generalized thinker, right.

**36:14** · And all of these steps, breaking down a problem, being able to backtrack, being able to do analysis, all of these are these skills that the model has learned during this thinking optimization process that now generalize to other things.

**36:31** · And they're helping the model right now.

**36:33** · So I think the other way to look at it is as Azalia presented, repeated sampling.

**36:37** · So if you had just a base model right after pre-training, it would be able to do some reasonings.

**36:44** · But at the same time, it will generate different kinds of reasoning chains.

**36:47** · And it doesn't quite know which one is correct.

**36:50** · So a lot of what we will cover in train time or test time scaling really comes down to it learns, which is correct.

**36:57** · So pass it, one accuracy goes up, which is what you were seeing in the reasoning models.

**37:01** · As opposed to pass it k or coverage, which is what you were seeing in the repeated sampling results.

**37:07** · Yeah.

**37:07** · And one other way to think about it, yes, these deep thinking and things that the model generates is actually helping the model every time to solve a new problem.

**37:22** · And although it's very expensive for the model to generate those things, still, we want them to generate those, because it leads to better answers.

**37:35** · Any other questions?

**37:37** · Yes?

**37:37** · Can you use a different model for the reasoning step versus generating the final answer?

**37:42** · Maybe a smaller or a purpose built one just in case the final answer is a large problem?

**37:49** · So typically, the reasoning capabilities have gone up with the model size.

**37:53** · So if anything, you would use the larger reasoning traces.

**37:58** · And then maybe you collect a bunch of reasoning traces and then have a smaller model summarize the answer.

**38:04** · So the models, this is at least currently, things may change, they like their own traces more.

**38:10** · Even if the traces are coming from a better model, they tend to their traces, their own generated traces, more.

**38:19** · And we're going to have talk about Swirl.

**38:21** · This is one of the papers that-- The multi-step reasoning.

**38:25** · The multi-step reasoning that we talk about, what if we bring a different model not in the context of generating reasoning traces, but in the context of evaluating and giving feedback?

**38:36** · And we're going to see that as well.

**38:38** · But models, surprisingly or not surprisingly, they like their own traces a lot more.

**38:44** · For reasoning models, how are they taught to reason?

**38:48** · Is it a hard coded set of sequences that are taught to do traces, or are they somehow fine tuned to say, we need to do this much or this kind of thing, which will cause the traces to generate?

**38:59** · So I don't think there's a published piece of work that really covers this bit.

**39:03** · It's both, yeah.

**39:05** · But it's a bit of both.

**39:06** · And at the same time, the base model did have the thinking capability to begin with, right.

**39:12** · Go do some amount of thinking.

**39:14** · One thing that we will cover in the class is this notion of outcome rewards model and process reward model, and how you can use that feedback to get the model back.

**39:24** · Yeah, there's always some bootstrapping.

**39:27** · Like, OK, here are different ways.

**39:29** · Chain of thought itself, which is heavily used in the instruction tuning of data set, shows the model some ways of how to think.

**39:39** · And there could be some templates showing for the model, fine tuning.

**39:44** · But the things that the model, if you just ask it any question and it comes up with that, there's a whole lot of generalization that.

**39:51** · So models have gone way above like what the data or instructions that are used for training them.

**40:00** · Yes?

**40:02** · In sampling, is there a way to make the number of samples from-- Please speak up.

**40:08** · The number of samples, can they be dependent on problem difficulty?

**40:13** · I don't think there's a published piece of work that does that.

**40:21** · So there is follow up work to that where we use a reward model, and then you can use that.

**40:27** · So assuming the reward model has some notion of complexity.

**40:30** · If you haven't solved, it can guide more sampling, or whether it's repeated or parallel.

**40:36** · But that's definitely an interesting direction to explore.

**40:41** · Yeah.

**40:43** · OK, we need to get to the-- oh, we haven't-- yeah, let me cover this.

**40:49** · OK, so you now know about large language models.

**40:53** · And then you heard about how they learned how to think, and then they learned how to reason.

**40:58** · So what's next, and why is this course relevant?

**41:01** · So a lot of what this course is about is that large language models, as chatbots or as reasoning models, are basically still single turn or just in the chat format.

**41:12** · So they're not accomplishing a task for you.

**41:14** · They're fun to interact with, but they're not necessarily accomplishing a task for you.

**41:18** · What has happened this year almost in the last few months, and it's been surprising, is that agents like Cloud Code or Deep Research have really enabled people to do real world workflows.

**41:30** · So they're agentic workflows which can achieve tasks that you ask them to do end to end.

**41:35** · So, for example, if you want to go research and figure out, where should I rent a home perhaps for the entire year, if I want to take a class at Stanford, the model would actually be able to do a whole bunch of analysis and go look at a lot of different websites and actually summarize the results and give you pros and cons of different places.

**41:57** · This used to not be possible before.

**41:59** · So this will cover a little bit of how that becomes possible and how this course allows you to learn about that.

**42:05** · And then Cloud Code for example, if any of you are Codex, which is the coding agent from OpenAI, if you're using that, what you'll see is that just by giving instructions in English, you can modify files, or you can figure out test cases and whatnot.

**42:20** · So it really has become a coding productivity tool in the day-to-day workflows for software engineers at this point in time.

**42:28** · So what is the transition from LLM to agents?

**42:31** · So as I was giving you the example of deep research and of coding agents, basically now, the model can be given a goal.

**42:41** · And it will plan out the steps that it will go interact with the environment.

**42:46** · And based on the feedback, it will correct its steps until it achieves the goals or it will come back and say, I cannot achieve the goal.

**42:53** · So this notion of having some notion of a goal, taking actions towards that goal, getting the feedback, and then deciding when to stop, that's what makes agents different from the chatbot types of what we were doing before.

**43:08** · And this also might require interacting with tools which are external to what the model itself is doing, getting some inputs from there.

**43:18** · But it still stays on track of whatever task it's choosing to accomplish, which might mean that it has to have some form of memory to keep track of the tasks that it's trying to accomplish.

**43:30** · So what has been accomplished?

**43:32** · So in several cases, in simpler cases, you can achieve these end to end goals.

**43:39** · Deep research can be accomplished end to end.

**43:41** · But in most scenarios, you are still having very static workflows.

**43:44** · So today, what exists is closer to agentic workflows, where you have some sort of an input where you're giving a model the goal.

**43:51** · And then what this slide is showing you is that one model is perhaps giving the output like a solution, and then another model is judging it and then deciding based on that, whether the solution should be accepted.

**44:04** · So that's one orchestration framework that's possible.

**44:07** · Deep research would be more of the second one, where you basically generating-- you're calling the LLM on multiple possible inputs and then aggregating the things to get the output, which will be a summary of the deep research results.

**44:22** · So this is a very cartoonish abstraction of what agentic workflows might look like.

**44:27** · And you can generalize from there.

**44:28** · But instead of having very open ended loop that I was showing you here, where you're supposed to go take an action from the environment and come back and do some feedback, it's easier for open ended problems to construct this graph by hand of how a human would do it and then get this feedback perhaps from an LLM, which is the LLM evaluator here.

**44:50** · So a lot of the real world workflows still have this paradigm.

**44:54** · But in certain cases, we are starting to see signs of life for what's possible in this slide.

**44:59** · And coding being one and research being another one.

**45:03** · So typically, the workflows will have things like LLM calls.

**45:07** · So you would basically call an LLM with an instruction or some form of input.

**45:11** · And then you're asking the LLM to give you an output.

**45:14** · It will have some form of verifiers.

**45:15** · We'll cover verifiers in a whole lecture by itself.

**45:18** · It will have some form of critics or judges, which is effectively LLM as a judge paradigm.

**45:24** · There might be tool calls.

**45:25** · For example, for deep research, you have to actually go search the web to figure out what exactly is the content that you should be looking at.

**45:33** · So there might be tool calls of that form or getting some value around what exactly is the weather.

**45:41** · And similarly, search would be another tool call.

**45:44** · And then you would orchestrate these in some form of a workflow.

**45:47** · So a simplest workflow here would be prompt chaining.

**45:50** · So similar to reasoning models where the task gets decomposed into subtasks, prompt chaining would simply be like you have chained a bunch of different subtasks that you're supposed to go accomplish to achieve the end to end goal.

**46:02** · There might be routing.

**46:03** · Routing works for complex tasks where you say, OK, if this is very complex, then go do this more complicated set of LLM calls.

**46:11** · And it's less complicated than do this simpler workflow.

**46:15** · There might be parallelization where deep research is one example where you can have multiple LLM calls work simultaneously on researching different keywords that you give as input to the LLM.

**46:26** · And then finally, you aggregate the output.

**46:29** · Or you might break the task into independent subtasks and then combine the solution.

**46:34** · Or you might have this notion of orchestrator, where you basically are actually using some sort of a, in simple words, LLM manager.

**46:43** · So a central LLM is actually doing the planning.

**46:46** · So in Cloud Code, you actually start to see that, that there is some notion of a plan that it comes up with.

**46:50** · And then based on that plan, it will make subsequent LLM calls.

**46:55** · You might have an evaluator or a judge.

**46:57** · So instead of getting feedback from real world, like user or from some sort of a actual running a unit test, it actually might just use LLM as a judge.

**47:05** · And we will have some homeworks that will cover this aspect.

**47:09** · And then you might have verifiers.

**47:11** · Verifiers are things where you can actually verify the output.

**47:14** · So in code, for example, if you run the code, how do you know that this code is correct?

**47:19** · So typically, as software developers we write unit tests.

**47:22** · So similarly, verifiers might be running some kind of unit test to check, whether what LLM generated is correct.

**47:29** · And in domains which are verifiable, math, code, and other domains that are more rule based, this verification is a good way to give feedback back to the model so that it can correct its steps.

**47:42** · So most of these workflows mean that the LLM needs to be better at planning.

**47:49** · It needs to be better at multi-step reasoning, and it needs to be better at self-improvement.

**47:52** · Like when it makes mistakes, it needs to be able to correct itself.

**47:55** · So effectively, these are new paradigms that the current set of LLMs just with reasoning were not quite accomplishing.

**48:04** · And these are some of the topics we do plan to cover in subsequent lectures.

**48:09** · And just to drive the point home around coding agents.

**48:13** · So this is a very simple example.

**48:17** · I should have updated the slide for Cloud Code.

**48:19** · But basically what this is showing is that you have an LLM agent and it's interacting with the computer.

**48:25** · These days just with the terminal, you give it an instruction where you might tell it that you want to implement a test.

**48:31** · And then it has some navigation of repositories, searching of files, all of these tool calls around viewing files, editing lines.

**48:39** · And then it will go execute a bunch of commands in the terminal.

**48:42** · And based on the output, it might be like, OK, I need to go edit this other file, or I need to go look at this other file.

**48:48** · So if you look at this loop, this very much mirrors what was-- so this was not quite reliable last year.

**48:55** · And it's just starting to get reliable in what we are seeing in the realm of coding agents now.

**49:00** · Yes?

**49:01** · Can I ask why do you think it's not reliable?

**49:05** · The general architecture is, I would say, not changed that much.

**49:11** · I mean, I think the paradigm is very much the same.

**49:14** · It's mostly a matter of more powerful models and then better RL.

**49:20** · RL with verifiable rewards is working.

**49:22** · The train time scaling is working well.

**49:25** · I see.

**49:26** · How did you \[INAUDIBLE\]?

**49:37** · I mean, computer data, right.

**49:40** · One of those two.

**49:41** · But just also, once the models start to get better, there's this self-improvement loop that kicks in.

**49:47** · Because you can now generate tests, and the tests become more reliable.

**49:51** · So in the published pieces of work, if you look at, say, code monkeys, which we covered last year, if you can generate unit tests for whatever code the model generated and then see if the generated unit tests are making things better, then that's a very good way to verify things, right?

**50:09** · Yeah, model based.

**50:11** · It seems like to some extent, if we have good verifiers, we can make the model generate the right code.

**50:21** · But the question is, how do we do that?

**50:23** · And there are ways to do it.

**50:25** · And we would be happy for you guys to take research projects in that domain, too.

**50:31** · But obviously, it's an active research area.

**50:34** · But there are ways to make improvements that-- I think what you're alluding to is this notion of generator verifier gaps.

**50:41** · So it's easy for models to generate a whole bunch of nonsense or sensible set of reasoning traces or useful set of content.

**50:49** · But at the end of the day, whether that's useful or not, we need feedback loop for that.

**50:53** · And if you're creative writing, how much feedback can you get?

**50:56** · So human feedback ends up becoming a bottleneck.

**50:58** · In domains where you can have good feedback, that's where it's possible to continue to improve the model.

**51:03** · And that but we're getting robust verification, a lot of robust verification is hard.

**51:08** · So Azalia will cover a paper that she did in her lab about how to combine verifiers.

**51:14** · But verification continues to be one of the bottlenecks in this space to make them better.

**51:20** · Yes?

**51:22** · Intuitively, I think free training, you get ability to survive at such a large corpus.

**51:29** · So just to me, intuitively, I'm trying to figure out why there's such a big jump.

**51:33** · Because we're providing a reward signal, and we're trying to elicit activities that shouldn't exist in training.

**51:43** · So I guess I'm just not-- I think this is still an active area of research.

**51:51** · So there are different set of opinions around what really improves the model.

**51:55** · Is it RL, or is it the pre-training, the diverse data by itself?

**52:00** · And I don't think there is a single point of consensus.

**52:02** · At this point in time, both processes help.

**52:06** · What you just said, which I will repeat for the class, is that if pre-training is the place where the model, after repeated sampling, should be able to at least have one solution correct out of if it was generating a large number of samples, then this notion of giving feedback should improve the passive one accuracy, but should not improve the model.

**52:24** · Why is it such a big jump?

**52:26** · But I think that whole loop is not completely well understood.

**52:30** · It's like the first signs of life and it starts to get commercialized.

**52:33** · But I think there's a lot more research still open in this area.

**52:36** · Yeah, that's right.

**52:37** · So that's only one way of thinking about it.

**52:39** · There are at least some signs of life which say that you can continue to do RL, and that will continue to improve the model.

**52:47** · Yeah.

**52:50** · OK.

**52:51** · Yeah.

**52:53** · So this is basically covering a lot of the same set of points.

**52:57** · But one abstraction that is worth taking away from this particular chart is that even when you give the model a goal, it has to clarify the user intent.

**53:06** · So it's not always obvious to it what the model user wants.

**53:09** · And then it might go search for relevant files.

**53:12** · And then whatever a set of actions which chooses to take, oftentimes, it needs some form of verification.

**53:18** · In this particular case, it's based on passing the test.

**53:22** · And it might actually generate the test that it needs to pass, which is also mentioned here.

**53:29** · But the key idea is that if you give it a task, how does it come back, and how do you know that it's going to complete what you asked it for?

**53:37** · Oftentimes, the users will not specify the problem well enough.

**53:40** · So clarifying the user intent so that it knows what to go look for and how to verify starts to become important.

**53:47** · And in models like O3, I think they have seen a lot of these traces end to end.

**53:51** · So they are able to do the planning, the reasoning, the multi-step reasoning, and come back with the conclusion.

**53:56** · But a lot of this is needed for completing tasks end to end or having an end to end goal.

**54:03** · And where this has been super useful is if you have repetitive tasks like code migrations or version upgrades, or if you need to restructure the code base.

**54:13** · Or if you have tasks that involve data engineering, where you have to basically do some sort of extract the data and then do some sort of cleanup on the data.

**54:22** · Or if you have to do some sort of data warehouse migration.

**54:25** · So a lot of this work tends to be extremely repetitive.

**54:29** · And it's much easier to just delegate it to coding agents.

**54:33** · Same for unit tasks.

**54:34** · Oftentimes much easier to start to give it to coding agents.

**54:39** · Another area where agents have become extremely prevalent is in customer support.

**54:44** · It's one of the most thankless jobs that when you are on the customer support side of things have to do, and using LLMs to do that definitely streamlines the experience in interesting ways.

**54:55** · So one simple set of examples ends up being like you can use them to do live transcription.

**54:59** · So that gives you a very nice record.

**55:01** · And you're seeing that even for meetings these days.

**55:04** · Another simple example is that you can have Knowledge Assist.

**55:08** · So if you have a database of information, the customer support agent does not need to know everything.

**55:13** · They can consult with the LLM and get an answer and surface the relevant article, which is better than having just search, an index and search by itself.

**55:26** · Smart reply.

**55:27** · So in chat, oftentimes, this has existed for a while, but you can use an agent to give chat responses.

**55:34** · And then having a call summary can help you-- you can use the call summary to really improve the customer experience by itself as well.

**55:43** · So overall, I think in the customer support area, there's multiple companies that are going after this area.

**55:49** · But there are different segments of the problem that can be addressed using LLMs, and they have been super useful.

**55:54** · And then there's also the end to end stuff that's starting to happen here.

**55:59** · And then the third example that we will use and actually some of the homeworks is that if you have very complex topics and you want to provide a comprehensive report, earlier, it used to be that you had to do a literature review, and then you had to summarize each paper, and then you had to synthesize these things.

**56:14** · And these days, you can just give it to an LLM and actually do it for you.

**56:17** · In the study, maybe more articles than you would.

**56:21** · So typically, if you give it an example like, say, 2022 Winter Olympics opening ceremony, it will identify what references to go look at.

**56:30** · Then it will construct an outline of, OK, these references are relevant or not.

**56:34** · And then summarize each of the references as to what is the relevant content, and then combine them to create a full length article.

**56:42** · Which is very impressive in certain cases, and you'll get to try it in one of the homeworks.

**56:49** · And then even more forward looking.

**56:53** · These research agents are starting to be used as AI scientists.

**56:58** · So basically, they're starting to assist scientists in, say, solving math problems or solving science problems.

**57:04** · So here, the LLM is used as a brainstorming thing to come up with ideas.

**57:09** · So the idea generation phase, then the experiment iteration phase, it might actually help you iterate on the experiments that you are hoping to work on.

**57:17** · This is from the AI scientist paper.

**57:19** · And then in the paper writeup phase, it will help you improve the paper writer by itself.

**57:27** · And what's interesting is that even though these models hallucinate just the notion that they can come up with so many different set of ideas, as an AI scientist, it might actually brainstorm or give you ideas outside what you would have thought if you had just taken a bunch of courses or if you're a researcher and you've been in the field for a long time.

**57:49** · Sometimes reading the web allows these alarms to come up with ideas that are way outside the box and can be a very good brainstorming way.

**57:58** · So these have been super useful in the AI scientist style of work.

**58:04** · OK, so let's move to course logistics.

**58:07** · But before that, do we have any questions?

**58:09** · Yes?

**58:11** · I just want to clarify.

**58:12** · So is reasoning and chain of thought linked in training, or is it just a prompt engineering that was accidentally discovering these kind of capabilities in larger models?

**58:22** · And if so, are there other emergent behaviors, sites, or reasoning that you think might be discovered?

**58:30** · So I mean, it was not baked in by design.

**58:35** · It was basically discovered.

**58:39** · I mean, we gave it hard problems, and then we saw that it was basically-- by having reasoning chains, it was doing better.

**58:45** · So the GSM 8-K was the first paper that showed signs of life of this.

**58:49** · And then with larger model like PaLM, we actually saw that this was a very big deal.

**58:55** · In one of the examples there was that it could explain jokes, which was very impressive.

**58:59** · And then from there, the reasoning models have emerged.

**59:03** · But it has read all of the web, so it has definitely seen data, which is more methodical and systematic.

**59:11** · But the reasoning models are trained to be reasoning more and more, right.

**59:18** · The entire reasoning is not an emergent behavior.

**59:21** · The reasoning models, they're trained to be thinking.

**59:25** · But the models are converging.

**59:27** · So the models are going to be trained such that they know when they need a lot of reasoning and when they don't.

**59:32** · And to generate the answers.

**59:35** · But chain of thought originally was an emergent behavior.

**59:39** · They noticed that, oh, if we explain things, a model gets better.

**59:45** · Are there any emergent behaviors in larger models?

**59:49** · I don't think I would see it as emergent behaviors per se.

**59:52** · But I think as I was mentioning, we usually go looking for certain things, right.

**59:55** · So in the agentic workflows, what we're looking for is planning, which is a form of reasoning.

**1:00:00** · We're looking for multi-step reasoning, which we will cover in class as well.

**1:00:04** · And then we're looking for self-improvement or self-correction.

**1:00:07** · So all of these capabilities would be nice to have.

**1:00:09** · And what gets the models there is a set of questions that are worth-- there are papers on this kind of thing.

**1:00:16** · Like self-correction, backtracking, things like that.

**1:00:19** · It's like yes, you could call it emergent, but you could also say, think about it, that they have seen this kind of behavior.

**1:00:28** · And it's like it's reinforced in the way that they're fine tuned.

**1:00:32** · So yeah, it's hard to say.

**1:00:38** · OK, so let's go through the logistics for the class.

**1:00:45** · Here's a list of all the amazing topics that you're going to learn about.

**1:00:52** · Yeah.

**1:00:54** · This is very cool.

**1:00:55** · I think the main thing to remember here is that the overall theme stays the same.

**1:00:59** · And then we'll also have guest lectures around from folks in frontier AI labs and covering things all the way from say, how has post training evolved, or even multimodal agents in robotics.

**1:01:13** · So it's going to be a mix of lectures and guest lectures.

**1:01:18** · And of course, your project presentations.

**1:01:23** · So here is some logistics that you all know.

**1:01:26** · The prereq are there.

**1:01:28** · Just make sure that you are comfortable with these prereqs as you register in the class.

**1:01:35** · So we have the external website.

**1:01:38** · But make sure that you check Canvas.

**1:01:43** · That's where we send out the latest updates at all times.

**1:01:47** · And we try to upload the lectures before we start in every class, so you have access to the lectures.

**1:01:57** · And we already have the due dates for all the assignments and all the projects.

**1:02:02** · So you can check it out.

**1:02:05** · So this quarter, we are going to have three homeworks.

**1:02:08** · That's a difference from between this class, and that's one of the differences.

**1:02:13** · So we have one more homework for you all that we have designed.

**1:02:17** · And the TAs have done a great job.

**1:02:19** · And that helps you hopefully learn these topics better and more in depth.

**1:02:27** · And then we also have a course project.

**1:02:29** · So the course project is where you can unleash your creativity and your way of building agentic systems or going deeper into a question and designing experiments around it and see what works and what doesn't.

**1:02:47** · We will provide some examples or suggestions, but it could be completely on you how to design this project.

**1:02:56** · You will have some examples from last year, like the successful projects from last year as well.

**1:03:02** · It's going to be uploaded to Canvas or-- Actually, we'll display them on the website.

**1:03:08** · Oh, on the website.

**1:03:09** · Oh, cool.

**1:03:09** · The public website, so you can also see that.

**1:03:13** · So yeah.

**1:03:14** · So for the course project, I think the main thing to remember is that we will have API credits, and you can work in teams of two to four people.

**1:03:23** · Right?

**1:03:24** · Yeah.

**1:03:25** · Or up to four, I guess.

**1:03:27** · Up to four?

**1:03:28** · OK.

**1:03:28** · You can be one if you really want that.

**1:03:30** · We suggest you team up with others.

**1:03:35** · At the very least, you have more credit collectively so you can run more experiments.

**1:03:39** · But then you might also find a friend collaborator along the way, and you can do something bigger.

**1:03:48** · And we are going to have this-- what is this?

**1:03:53** · The course project.

**1:03:54** · Yeah, we're going to let you know about some of the previous years and some ideas that you can take.

**1:04:01** · Here are some course project examples that are acceptable.

**1:04:05** · For example, a new evaluation data set or a new benchmark.

**1:04:10** · You can design a project around the reliability of an agentic system that already exists.

**1:04:17** · You can take a benchmark that exists and try to hill climb on it with whatever idea, great idea that you have.

**1:04:25** · And then or you can just-- we are going to have a whole lot of papers covered in this course.

**1:04:30** · And we are showing all of that to you.

**1:04:33** · They're all on the website.

**1:04:34** · So as we give these lectures, we expect you to also have read those papers or read the papers along the way and develop better and deeper intuitions on how these methods work.

**1:04:46** · And your project could always be improving those or questioning one of the decisions that they have made and trying to change that or evaluate that.

**1:04:58** · Negative examples are like a survey paper.

**1:05:03** · We want something researchy here.

**1:05:05** · So we just don't want just an app that you put together and you just show us something.

**1:05:10** · It has to be like, here is the hypothesis.

**1:05:14** · Here is the question that we wanted to answer.

**1:05:16** · Here is the type of improvement we wanted to see or the type of properties we wanted to analyze.

**1:05:23** · And then we have built that.

**1:05:24** · Right, we want something that-- something more than white coding, basically.

**1:05:32** · In terms of milestones, I think it's worthwhile to remember that you want to start early.

**1:05:37** · So you need to have a project proposal somewhere around-- I think we put it early October.

**1:05:44** · And then-- It's on the website, yeah.

**1:05:47** · It's on the website.

**1:05:48** · And then for the midterm project presentation, we do want you to have some progress.

**1:05:52** · So two weeks after the project proposal, we do expect you to have-- so start thinking about what experiments you want to run by the time you get to the project proposal so that you actually go run them for the midterm projects.

**1:06:04** · So we do expect you to have made some progress in the midterm project presentation.

**1:06:08** · It should not just be, here is a proposal.

**1:06:11** · And then the final report has a lot of weight.

**1:06:13** · And then the final poster presentation will be the end of the quarter.

**1:06:21** · Yes.

**1:06:22** · Let's see if we do a \[INAUDIBLE\].

**1:06:40** · I think so.

**1:06:42** · If you add to it, right.

**1:06:46** · \[INAUDIBLE\] is independent study, right?

**1:06:49** · Yeah, independent research.

**1:06:50** · Yeah, yeah, that's fine.

**1:06:51** · I think-- I mean, as long as you're doing actual work and it's not just like reusing the work from an exact copy of something, yeah.

**1:07:01** · We had students publishing papers out of their projects in the last quarter.

**1:07:08** · So in the last time we taught the class.

**1:07:11** · So that's something we could be one of you or many of you this time, again, turning your research project, working more on it, and then turning it into a publication at conferences.

**1:07:27** · And so here is a save the date for our poster presentation.

**1:07:33** · It's going to be December 12, 4:00 to 6:00 PM.

**1:07:36** · So we would want you to be there and present the posters.

**1:07:40** · We'll have people from industry joining.

**1:07:44** · That's where you can brag about what you've done and just meet new people.

**1:07:48** · Here is the course grading rubric.

**1:07:52** · So we have three homeworks.

**1:07:54** · That's 50% of your entire grade.

**1:07:58** · And then another 50% is on the project.

**1:08:01** · And the duration of these are aligned with how much the grading is allocated to each of these.

**1:08:10** · And we, of course, expect you to honor the honor code.

**1:08:17** · And let's see, office hours will be posted on Canvas.

**1:08:23** · You can ask your questions.

**1:08:25** · We really, really encourage you to ask questions on Edson and make it public.

**1:08:30** · Probably if you have a question, it's very likely others have the same question.

**1:08:35** · So please help us do broadcast this to everybody.

**1:08:40** · Edson is, again, you can ask questions, and then Gradescope is where you submit your project milestones and everything else.

**1:08:50** · Yeah, the homeworks and everything.

**1:08:52** · We have the following late policy that we think is within the generous-- on the generous side of things.

**1:09:03** · And because the class is big this quarter, we really can't make any exceptions.

**1:09:09** · So try to use these late days wisely.

**1:09:15** · Audits are not allowed, but we will have the course-- we will have the videos-- Videos on YouTube, eventually.

**1:09:24** · Eventually.

**1:09:26** · And that's it.

**1:09:27** · Any questions?

**1:09:32** · No?

**1:09:34** · All right.

**1:09:35** · OK.

**1:09:35** · Thanks, everyone.
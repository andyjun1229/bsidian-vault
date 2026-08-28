---
title: "Stanford CS329A Self-Improving AI Agents | Part 9 | Future Research Areas"
source: "https://www.youtube.com/watch?v=AyO6wyu4DEg&list=PLangBM27OtEA&index=9"
author:
  - "[[Stanford Online]]"
published: 2026-08-03
created: 2026-08-26
description: "Want to dive deeper? This curriculum is covered in the following online courses:- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html- XCS329 graduate course:"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=AyO6wyu4DEg)

Want to dive deeper? This curriculum is covered in the following online courses:  
\- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html  
\- XCS329 graduate course: https://online.stanford.edu/courses/cs329a-self-improving-ai-agents  
  
A similar curriculum is covered in XCS329z https://online.stanford.edu/courses/cs329z-engineering-ai-agents  
  
Follow along with the course schedule and syllabus: https://cs329a.stanford.edu/  
  
View the course playlist: https://www.youtube.com/playlist?list=PLangBM27OtEA  
  
Video Summary:  
This final lecture video of Stanford's CS329A, Self-Improving AI Agents, taught by Aakanksha Chowdhery and Azalia Mirhoseini on December 5, 2025, covers open research directions in self-improving AI agents. Chowdhery presents three papers on bottlenecks in self-improvement loops: Multi-Agent Fine-Tuning, which uses specialized generator and critic agents to produce diverse reasoning chains; Deep Math V2's meta-verification approach for automated proof checking without reference solutions; and Absolute Zero, a method for models to propose and solve their own coding tasks through self-generated reasoning challenges without external data. Mirhoseini then presents research on the intelligence-per-watt metric, showing that local models with 20 billion parameters or fewer can now handle 88.7 percent of real-world chatbot queries, a 5.3 times efficiency gain over two years from combined model and hardware improvements. The lecture closes with open questions on continual learning, test-time scaling infrastructure, and hybrid local-cloud inference, along with a discussion of non-verifiable domains such as chip design and scientific simulation where reward models substitute for slow ground-truth verification.  
  
Speaker Bios:  
Aakanksha Chowdhery  
Adjunct Professor of Computer Science, Stanford University  
  
Dr. Aakanksha Chowdhery is pushing the frontier of agentic LLMs, focusing on recursive self-improvement and long-horizon agents that learn and deploy in the real world. She is one of the few researchers globally who has led frontier model training end-to-end, across both dense and mixture-of-experts (MoE) architectures. At Google, she led the 540B PaLM model, the largest densely trained language model in the world at the time. She subsequently drove pre-training and scaling of Gemini's MoE models across multiple generations, and contributed key components to PaLM-E, Med-PaLM, and the Pathways infrastructure underpinning Google's large-model efforts. She went on to build and lead pretraining teams for open intelligence efforts at Reflection and Meta. Earlier, she held research roles at Microsoft Research and Princeton. At Stanford, where she earned her PhD, she teaches CS329A (Self-Improving AI Agents) and serves as Program Chair for MLSys 2026.  
  
Azalia Mirhoseini  
Assistant Professor of Computer Science, Stanford University  
  
Azalia Mirhoseini is a co-founder of Ricursive Intelligence, a frontier lab dedicated to recursive self-improvement through AI that designs the chips that fuel it. She is also an Assistant Professor of Computer Science at Stanford University where she directs Scaling Intelligence, a lab focused on developing scalable and self-improving AI systems and methodologies toward the goal of artificial general intelligence. Previously, she spent several years in industry AI labs, including Google Brain, Anthropic, and Google DeepMind, working on the development of Claude and Gemini. Her past work includes Mixture-of-Experts (MoE) neural architectures, now predominantly used in leading generative AI models; AlphaChip, a pioneering work on deep reinforcement learning for layout optimization used in the design of advanced chips like Google AI accelerators (TPUs) and data center CPUs; as well as pioneering research on LLM Test-Time Scaling. Her work has been recognized through the Okawa Research Grant, the Google ML and Systems Junior Faculty Award, MIT Technology Review's 35 Under 35 Award, the Best ECE Thesis Award at Rice University, publications in flagship venues such as Nature, and coverage by various media outlets, including WSJ, NYT, Forbes, MIT Technology Review, IEEE Spectrum, WIRED, and TechCrunch.

## Transcript

**0:05** · So we will start with an overview of what we have covered in this quarter.

**0:13** · So we started the class with just giving you an overview of LLMs and how over the past year, test-time scaling and train-time scaling using self-improvement techniques where the fundamental loop is driven by verifiers, and feedback from running those verifiers and getting rewards, and then using reinforcement learning and even search algorithms to help the models to climb on math and coding, for example, have been a lot of the focus of initial part of the class.

**0:45** · From there, we started talking about evolutionary strategies.

**0:48** · So there was a whole class on open-endedness where we're not just driving self-improvement loop with rewards.

**0:56** · We also allow the model to just go explore if the exploration space can be defined.

**1:02** · And here we discussed alpha evolve and similar techniques.

**1:07** · Then we moved to a paradigm where we build end-to-end workflows for agents using tool-use.

**1:14** · And as the models interact with environments and tools, you basically are able to drive the workflows end to end.

**1:22** · And if you imagine that if you have tasks that need to be completed over multiple steps, then you do need to have perhaps the ability to look at knowledge bases.

**1:32** · So that requires retrieval and memory.

**1:35** · So basically, as we go towards real-world workflows, we need better planning and multi-step reasoning in these models.

**1:44** · So we discussed some works around that and how to really look at evaluations in the next generation of models and what capabilities would drive that.

**1:55** · And then we had several guest lectures on post-training and multimodal agents and robotics and reasoning and so on.

**2:03** · Azalea, is there anything you would like to add here?

**2:07** · Yeah, I think this sounds good.

**2:09** · This is full coverage.

**2:11** · So one of our guest speakers also talked about the symbolic techniques, which goes under the umbrella of tool use and how that could add to the synthetic data, which is another trend we are seeing.

**2:25** · Amazing.

**2:25** · Thank you.

**2:30** · So I think just to recap and this-- the class is named as self-improving agents.

**2:36** · So it's not just focusing on LLMs.

**2:38** · It's focusing on the agent aspect of it.

**2:40** · What that roughly-- if we were to remind you of what we discussed in first class, is that how is an agent a generalization of LLM.

**2:50** · It has a goal and it will go and interact with the environment, collect feedback, and use that feedback to correct its steps.

**2:56** · So they're basically systems that can direct their own processes, use tools, and then accomplish a goal.

**3:03** · And oftentimes in the current paradigm, the LLMs by themselves are not powerful enough to drive towards a full goal.

**3:11** · They're getting there.

**3:12** · So oftentimes we would hand-write these systems as workflows where you are orchestrating LLMs and tools.

**3:20** · However, in certain scenarios like coding agents, you are seeing some of these agentic workflows being driven by themselves.

**3:28** · So it's an exciting time where we are seeing a lot of progress in this area.

**3:34** · And how we construct these workflows oftentimes means you're orchestrating LLMs, you're orchestrating verifiers because you need some form of reward.

**3:42** · You might have LLMs as judges for verifiers.

**3:45** · You might have tool calls.

**3:46** · You might have search algorithms in there.

**3:48** · So you might have parallel LLM calls that are going and doing these kind of search.

**3:53** · But overall, since an agentic workflow is driving towards the goal, It.

**3:57** · Needs the capability to plan and to reason over multiple steps, correct itself if it were going in the wrong direction, and overall keep improving in its capabilities, which is where the self-improvement aspect comes in.

**4:13** · So in this lecture, as we wanted-- we wanted to cover some future research areas.

**4:18** · So we organized it as key ideas from certain papers that both cover the self-improvement side of things and just generally the efficiency side of things for intelligence, both of which we believe are extremely important directions in the next research areas.

**4:38** · So for the first three papers that I will cover, I'll just present the key ideas.

**4:46** · But let me just present why those papers were chosen and what are the key ideas that they point in terms of next steps and directions.

**4:57** · So what we learned in the class is a lot about say, test-time scaling, where you could improve by having multiple samples and majority voting and so on, and then train-time scaling where you can use that feedback in the inference loop and get rewards to drive that self-improvement loop.

**5:17** · Oftentimes, this is still limited to narrow domains like math and coding.

**5:22** · So how do you get generalization across these domains, and how do you generally get those reasoning chains to be diverse enough so that you can continue to drive that self-improvement loop is something that is an important research area even now.

**5:38** · An important aspect of building these self-improvement loops continues to be verification.

**5:44** · So how do you have robust verification techniques or meta verification techniques where you verify what was going into the reasoning chain is often quite valuable.

**5:56** · So that's another area that the second paper I will present the ideas on will cover.

**6:01** · And the third aspect is that even though we talk about train-time scaling, the prompts that go into training these models gets selected very statically and require humans to select them.

**6:14** · So how do you break through the data barriers so that the self-improvement loop can pick the right set of data that drives that loop?

**6:24** · So that's going to be the first part of the focus.

**6:26** · And the second part of the focus will be focused on just what drives efficiency for intelligence, so intelligence per what aspects.

**6:35** · So let's take a quick look at some of the ideas that might drive this self-improvement loop further in the next generation of systems.

**6:44** · And given how fast the field is moving, maybe we'll be teaching papers on each of this next time.

**6:51** · So the first paper that we cover is coming from multi-agent finetuning, which focuses on self-improvement with diverse reasoning chains.

**7:00** · The key idea of this paper is that pre-training, compute, and instruction tuning is bottle-necked by-- so pre-training compute is a compression of internet scale data and instruction finetuning often requires real human data, where you need human preferences to decide what is good model response and bad human response-- bad model response.

**7:22** · So an alternative to this is that you can use the data generated by LLMs, which is often called as synthetic data.

**7:28** · And you can do iterative finetuning where you generate possible solutions and filter out the incorrect ones.

**7:33** · This is called rejection sampling and fine-tuned only on the good ones.

**7:37** · Now there are many variants, STaR and so on, which can help drive this loop even better.

**7:43** · We covered STaR in class.

**7:45** · You can even add reasoning chains in that process.

**7:49** · But what typically happens is that if you're using a single large language model to generate the data, then it will generate solutions that will be very similar.

**7:59** · And oftentimes the performance increase will stop after a few iterations or after tens of iterations.

**8:07** · And typically, this problem comes down to really the notion of lack of diversity.

**8:13** · So when you look at model training, at the pre-training scale, the data is so diverse because it was generated over such a long time by humans.

**8:22** · So it is quite diverse and that helps the performance.

**8:27** · But when a single large language model is generating outputs for a set of prompts, it will not have very diverse responses even at high temperatures.

**8:36** · So the intuitive solution for this often means that you can use multiple agents, which are specialized in some way, and then use them to improve the diversity.

**8:47** · So what this paper proposes, for example, is multiple specialized agents for generations that will then produce a diverse initial solutions.

**8:56** · So they train generation agents and critic agents.

**8:59** · So the generation agents will help generate a lot of diverse initial solutions, while the critic agents will evaluate and refine the solutions.

**9:09** · So those are specialists as well.

**9:11** · So if you were to look at step-by-step process, and we don't need to go through every single detail in the algorithm below, but the generation agent will come up with an initial answer and then there will be debate over multiple rounds.

**9:26** · So what the generation agent will-- in the initial step, it will just have the initial answer, but in the subsequent steps, it will summarize and get a summary of all other agents responses and use that also as part of generating the next response.

**9:43** · The goal of the critic agent is to critique this updated set of answers.

**9:47** · So basically, if you're doing any iterations, there's an initial response from each of the generation agents.

**9:55** · Then you do a summary across all of these agents, and then the critic agent will critique this updated set of answers.

**10:01** · So it's very similar to what you guys were already familiar with.

**10:05** · The main difference here is that instead of getting the critique over a single agent's response, you're actually using multiple agents responses and then specializing and summarizing across them.

**10:19** · What this enables is that you have some form of diversity, even at the generation stage, before you're critiquing the answer.

**10:27** · So you basically get majority voting for free just by having multiple agents and assuming that these are trained slightly differently.

**10:36** · You get diversity for free.

**10:39** · So the generation models in this particular case are fine-tuned from the same base model.

**10:45** · And the goal there is to produce good answers given a question.

**10:49** · So over multiple iterations, what they're doing is they're taking outputs and filtering for a match with the majority vote.

**10:56** · And then doing SFT on this list of prompt and response pairs.

**11:00** · If you were looking at a very naive version of doing this, you could just use different models, which is something that people do in practice as well.

**11:08** · So they will get very different responses with different prompts.

**11:11** · So that's the poor man's version of doing multiple generations.

**11:17** · And the critic models in this particular paper was proposed as the critic models will basically take the updated answer and then select the best one.

**11:30** · So they are also fine-tuned.

**11:32** · And these are fine-tuned on a mix of trajectories where answer is correct at the start and then is corrected over a course of debate.

**11:40** · So basically, the critic model is learning how to contrast the correct and the incorrect answer.

**11:49** · So to summarize the whole process, there is n generation models and they are each producing an output.

**11:56** · The summarization happens.

**11:58** · You can imagine that either you summarize it with a model, or you can just concatenate the responses of all the models.

**12:04** · Then there is a critique process on that and that's added to the input.

**12:12** · And then you do a second round for all of the model generates outputs, updated answers, and then you do majority voting on top of that and again summarize the responses.

**12:23** · And you can continue this process in form of a debate in some ways.

**12:27** · So those trajectories can then be used to fine-tune different critiques as well.

**12:35** · So how does this help?

**12:37** · Why did we discuss this?

**12:38** · So I think the key metric that we're looking for is that on the x-axis, you're looking at how many iterations of fine-tuning it has gone through, and on the y-axis, you either have the negative log likelihood or you have the embeddings dissimilarity.

**12:54** · The negative log likelihood is just a proxy for performance.

**12:58** · And the embedding dissimilarity, the higher the value, the more diverse it is.

**13:07** · So what we see on the left is for two open source models.

**13:11** · When they go and do fine-tuning, they're actually able to continue to increase performance when they do this multi-agent fine-tuning.

**13:17** · And Llama seems more responsive to this technique.

**13:22** · I think the right side is more interesting.

**13:23** · As they're going through this process, the responses continue to stay quite diverse.

**13:30** · And this is over math as a data set.

**13:33** · And overall, they tried this again in math over three open source models.

**13:39** · And since they were going with fine-tuning, they had to stick with open-source models.

**13:43** · But with multi-agent techniques, they were able to continue to see improvements even over multiple steps of fine tuning.

**13:50** · While for single-agent fine-tuning, the accuracy collapses or doesn't continue to improve.

**13:58** · And they also show that not just in domain, which is math, in adjacent domains like GSM 8-k, this is a slightly older piece of work, so the numbers are not that high.

**14:10** · But even in adjacent domains like GSM 8-k, the fine-tuned agents actually show higher performance.

**14:18** · So this technique actually does help, so it generalizes beyond just in domain data sets that it's trained on.

**14:27** · So that's the first set of comments.

**14:30** · So what that roughly says is that if you want self-improvement, the reasoning chains that are provided to the model to drive those need to be diverse in some way.

**14:39** · And how you generate that one technique could be based on having multiple models or multiple agents generate those kind of chains.

**14:47** · A second problem that's very challenging, and we covered actually in the first few lectures is around verification.

**14:54** · So it's quite hard to verify model outputs.

**14:58** · And typically, you would just look at the outcome.

**15:03** · So if you have a math problem or a theorem proof, what you will look at is the final outcome.

**15:10** · And then you have an outcome reward model, so does that match the ground truth, and then you will say that this verifies.

**15:16** · One of the questions that we discussed in the verification lecture is that what happens if the reasoning chains are wrong, and will that lead the model astray, or will that cause some performance gap at the end?

**15:31** · And we also realize that process reward models are quite hard to build.

**15:35** · So DeepSeekMath-V2 is a recent paper that came out which tries to show that, at least in the theorem proving domain, it is possible to build self-verification loops, which are automated.

**15:47** · So that's a very interesting concept.

**15:51** · Just to remind you on what I was saying, the current reinforcement learning approach assumes that final answer will match the ground truth, and that's how you're basically creating the rewards.

**16:02** · So this has enabled saturation of multiple benchmarks like Amy or other math-related benchmarks.

**16:08** · But oftentimes, even when you have the correct answer, you might not have the correct reasoning.

**16:13** · And if you are actually trying to get the models to do better in theorem proving, you do require rigorous step-by-step derivation, which the final output doesn't quite give you.

**16:23** · Now, the interesting aspect is that the large language models are often trained on quantitative reasoning, so the proofs that they might generate are mathematically invalid.

**16:33** · And if you ask them to verify, they will claim that the incorrect proofs are valid.

**16:39** · So LLM as a judge technique doesn't quite work here.

**16:43** · But if you actually have expert humans look at these proofs, they will be able to look at the proof and reason about the fact that they know this area.

**16:53** · They can reason about the fact and say that, OK, this proof has issues.

**16:56** · It's just not making sense because this next step is not following from the last step or there's reasoning gaps in the proof solution.

**17:07** · So what DeepSeekMath-V2 proposes is that instead of just training the reward models, they train verifiers or meta verifiers basically.

**17:19** · So they get humans to identify issues in the proofs without any reference solutions.

**17:25** · And based on that, they train LLMs to identify issues in the proof and improve upon those.

**17:34** · And then if you will find that there-- so you basically have trained a model which can now critique the proofs themselves.

**17:41** · So what the final architecture for DeepSeekMath-V2 looks like, you folks are already familiar with the fact that there's a generator and a verifier, typically in the loop for building train-time scaling system.

**17:54** · So you have one model that is producing proofs and another model that is perhaps verifying things.

**18:01** · So it's identifying issues.

**18:03** · What DeepSeekMath-V2 adds is this notion of meta verifier.

**18:06** · So you have a meta verifier that will review the verifiers analysis for whether it makes sense or whether there are issues with the proofs.

**18:15** · And then the verifier is trained to take these issues and then score the proofs on a scale of 0.5 and 1.

**18:23** · So the verifier will then go improve the generator and the generator will produce harder proofs, which will then go improve the verifier.

**18:30** · So basically this ends up being a loop in some way.

**18:35** · And the other interesting aspect here is that because once you see the data for finding incorrect proofs, then you can actually automate that kind of labeling.

**18:46** · So you don't have to just rely on humans identifying issues in the proofs once the meta verifier starts to learn this.

**18:55** · So this notion of meta-verification is generally quite interesting in that verifiers can get correct score when the reasoning chains are incorrect.

**19:04** · For example, they might come up with fabricated errors.

**19:09** · So meta-verification has evaluation of this analysis to these issues that the verifier-- verifier here is LLM as a judge, or do these identified issues actually exist?

**19:21** · Does the score follow from the issue?

**19:24** · So they're basically analyzing whether the verifier did a good job or not.

**19:27** · And then they have experts annotate the quality of this evaluation.

**19:32** · And just by adding this additional block, they are able to improve the quality.

**19:36** · So it's almost like you had reasoning chains and then now you have the verifier over those reasoning chains, which is basically saying that, is this evaluation correct or not?

**19:48** · So there's an LLM as a judge, which is identifying the issues in this reasoning chain.

**19:54** · And then do those issues exist or not, is what meta-verification is looking for.

**20:02** · If you look at the results here, just with this iterative optimization, I think all of us are familiar that a lot of the RL loop often is built on top of TRPO.

**20:15** · In this particular case, they're building on top of DeepSeek-V3-based models.

**20:19** · So just the verification generation loop now benchmarked on IMO problems and CNML problems, the Gemini version of that was presented by one of our guest lecturers.

**20:34** · But this is an open-source version that was released recently.

**20:38** · They are able to show that in eight iterations just past one, the proof score continues to climb just with that iterative loop.

**20:47** · And then if you have best at 32-- best at 32 means you pick the best solution out of 32 generated proofs, there you are almost getting to 42% in proof score for IMO shortlist of 2024.

**21:01** · So this is quite promising as a hill-climbing technique, which roughly suggests that there is some promise if you can identify the issues in the reasoning chains and actually push the model or nudge the model towards correcting them.

**21:15** · So overall, the insights here are that the best proofs will achieve higher verification scores, and the generator can learn to differentiate higher quality proofs from flawed proofs.

**21:29** · And the self-verification as a result can basically have this better improvement loop.

**21:36** · So verification can be a bottleneck and this is one way to break that bottleneck.

**21:41** · Overall, I think if you were to try to generalize this technique in other areas, what you're basically looking for is if you have LLM-based verifiers, you need to find a way to get them to identify issues without reference solutions.

**21:56** · That's what this paper is relying on.

**21:58** · Then you need some form of an additional block, which is meta-verification so that it can reduce the chance of hallucinated issues that were identified by the verifier.

**22:08** · And then you add an additional incentive for the generator to maximize quality through deliberate reasoning.

**22:17** · So you're basically improving the quality of the model responses here.

**22:20** · So overall, this notion of self-verification is introduced by our DeepSeekMath-V2.

**22:26** · And it starts to break the bottleneck in verification if you can make that more automated end to end.

**22:35** · Of course, this is still limited by domains where verification is easier rather than more difficult.

**22:47** · So we covered through what is the diversity in reasoning chains and we discussed a bit about the verification bottleneck in the models where oftentimes to get the models to get over the bottleneck of verification, you would need some form of verification techniques.

**23:09** · And DeepSeekMath-V2 publishes that in open source.

**23:14** · A third problem that you have to solve is this notion of what data or what prompts should I train on.

**23:23** · So there's this very interesting paper that has not seen much use yet, but is quite promising and interesting is that you basically have the models propose the set of tasks that they should go train on that are just at the edge of what they have learned.

**23:43** · So to remind you, typically in the current AI training stack, you are either using human-curated reasoning traces, so that's for the supervised learning stage, or for reinforcement learning with verifiable rewards, you are expecting some experts to curate the question-answer pairs, but that basically requires that if you're constructing such a model in math, then you need math experts.

**24:09** · If it's an IMO problems, then you need IMO experts, or if it is encoding, then you need strong software coders.

**24:17** · So as the models continue to surpass human intelligence, the ability to find more and more experts and more and more such tasks starts to be limiting.

**24:30** · So what this paper proposes, and this idea is still very new, is that a single model can both propose tasks and then solve them.

**24:39** · So it almost goes to the other extreme of, we should not really need an external source of data.

**24:48** · So basically, we should not need human-generated prompts to climb on.

**24:55** · The model itself will propose the tasks and then it will go solve them.

**24:59** · And so that's a very interesting set of ideas.

**25:03** · And it is feasible in certain domains.

**25:06** · So they focus more on coding as a domain.

**25:08** · And they effectively construct three types of tasks-- abduction, deduction, and induction.

**25:16** · And I will explain this diagram in the subsequent slides.

**25:19** · But effectively, what this is saying is that in the proposal stage, they will construct the tasks based on this task types and then come up with a reward to select which tasks make sense.

**25:32** · And in the solution stage, they will verify and then have an accuracy reward.

**25:37** · And then that can help give a joint update on the model itself, as opposed to just one-sided updates.

**25:45** · So what is the proposer?

**25:48** · How is the proposer proposing tasks?

**25:49** · That's quite interesting.

**25:51** · So it's effectively based on coding paradigms.

**25:53** · So it's effectively saying that you have deduction tasks where you are generating a program and input and the environment is executing to get output.

**26:06** · So this is your usual come up with a program and an input pair.

**26:11** · And then the environment will execute to get outputs.

**26:15** · Abduction tasks-- they're similar to deduction.

**26:18** · You're generating the program and inputs and environment again computes outputs, but induction tasks are different.

**26:24** · It samples an existing program and then generates new inputs for it plus a natural language message describing the function, and the environment then goes and executes and decides whether this is going in the right direction or not.

**26:43** · And another interesting bit that I should mention here is that the proposer will be conditioned on past here.

**26:49** · So I'll cover that in a later slide because otherwise it will get confusing.

**26:54** · But it will be basically conditioned on past-generated examples that are explicitly prompted so that they're basically added to promote diversity.

**27:05** · So how do you select tasks?

**27:08** · The proposer will get a reward based on optimizing for task difficulty.

**27:13** · So if when the solver can-- so each of the tasks that are generated are passed to the solver.

**27:20** · And if the success rate is zero, then you get a zero reward.

**27:26** · And if the success rate is non-zero, then you basically get 1 minus average success rate.

**27:31** · And the kind of task that you want to select are the ones that are not trivial and the ones that are not impossible.

**27:38** · So there is some ability to continue to learn.

**27:40** · So you end up selecting tasks that are of moderate difficulty, where solver will sometimes succeed and sometimes fail.

**27:47** · And this will generally help with getting the model to learn.

**27:53** · So that's the goal of the proposer, is to generate tasks for optimal task difficulty at a current set of model weights.

**28:02** · And as the model becomes more capable, then the proposer should learn to propose harder problems.

**28:09** · Of course, if you generate tasks, then you need to somehow make sure that these are valid tasks.

**28:14** · So in the coding abstraction, one can run program integrity.

**28:18** · So you can actually execute these tasks and see whether there are any errors.

**28:22** · You can do safety checks.

**28:23** · You can also make sure that if you run these inputs multiple times, you get exactly same outputs because in code that's possible.

**28:31** · So the proposed tasks before it goes into the training pipeline is validated.

**28:36** · So that's one way to make sure that the proposal doesn't just hack and come up with garbage tasks.

**28:45** · And in terms of-- there's a buffer that is kept.

**28:48** · So for every seed triplet, there's an identity function like basically the input-output and the program for each of those triplet tasks, you're adding them to the task buffer.

**29:02** · And the proposal can sample references from that buffer.

**29:06** · So there is some sort of a buffer that is kept along with how many times the model is succeeding or failing on this.

**29:16** · So this is basically leading to this idea of curriculum learning that is evolving over time.

**29:22** · And why is this exciting or interesting?

**29:25** · I mean, on coding benchmarks, this notion starts to let you hill-climb despite having much human curated data which-- humans can generate a lot of coding data, but that after a while, synthetic data or some-- this is almost a play on synthetic data in some ways, but it's generating that in the loop at the task level as well.

**29:48** · So what they show is that they're able to get state-of-the-art on coding benchmarks, even though they didn't have any human-curated data on the prompt side.

**29:56** · And they are able to outperform models trained on tens of thousands of expert examples.

**30:02** · Some emergent behaviors that they show are that the complexity metrics increase over time so that can be expected if the proposer is continuing to increase the difficulty of what it's learning.

**30:13** · And another aspect is that the diversity of programs and answers, when the loop is set up correctly, is improving.

**30:19** · And the proposer is actually increasingly is generating more and more difficult tasks as the training is progressing.

**30:28** · So in some ways, it's almost like game theory where the proposer and solver are slightly adversarial, but overall, they are helping each other improve in some ways.

**30:38** · So this is solving to the bottleneck of which tasks to go train the models on.

**30:43** · So if you were to look at takeaways here, I think it's basically going down the path of the task selection problem on which these models run their self-improvement loop, should not get bottlenecked on human data, because otherwise you are very bottlenecked on which human experts, as long as you can have some form of verification there.

**31:04** · And you need some form of ability to do curriculum learning.

**31:08** · So this particular technique definitely relies on that.

**31:12** · And even though they only hill-climb on self-proposed code tasks, they actually see strong performance on both coding and math benchmarks.

**31:23** · So that's actually surprising that they are also seeing strong performance on math benchmarks, though one can explain that from other results that have been seen in the field.

**31:30** · And overall, larger models get bigger gains relative to smaller models.

**31:34** · So this is another idea in the space of improving the self-improvement loop that seems quite promising and continuing to hill-climb in that area.

**31:46** · Can I add something on the previous?

**31:49** · So I feel like we are seeing the same thing.

**31:52** · Like, we learned about SWiRL, the step-by-step RL with synthetic data.

**31:57** · I feel like the findings here and there really kind of resonate with each other in the sense that synthetic data like model generating its own training data can improve the model not only on the task that the generation is happening on but also in transferability.

**32:17** · Like in SWiRL, it was on, let's do a multi-hop question answering with retrieval.

**32:22** · But then as more synthetic data was generated and RL training was done, the model was getting better at other tool calling, like calling a Python and solving math problems, and vice versa.

**32:35** · So it seems like there is this clear kind of repeated trend that we are seeing in terms of synthetic data generation by the model and generalization.

**32:44** · And the other piece that's interesting, again, that kind of is the same kind of observation is that larger models seems to be better at absorbing this kind of data flywheel and also generalizing through that, especially when it comes to in SWiRL at least on the RL optimization side, which is an interesting observation.

**33:07** · Great, great.

**33:09** · Where would you take it from what you learned as well.

**33:13** · So I was going to summarize and you can add more bullet points.

**33:16** · I think to me, to achieve true generalization and reasoning, we really need that notion of diversity in the reasoning chain.

**33:25** · So that was the first set of comments I was making.

**33:28** · And how we achieved that continues to be an open problem.

**33:32** · We need better verification, and the more we can break that verify loop in a way where we are not bottlenecked by humans or tasks that are verified only through human experts, the better off we are in some ways, like building reward models is challenging.

**33:49** · And then I think the third is the selection of data itself.

**33:53** · There's only so much data that can be curated by humans for what prompts go in.

**33:58** · So breaking that barrier is also quite important in next generation of self-improving models.

**34:05** · What else you would add there?

**34:08** · Yeah, I think, one, just like based on these kind of existing work, something that would be interesting is that how much we can push the frontier of this self-improvement only based on the verifiable domains that we can generate synthetic data and bring it back to the model on diverse tasks, on diverse, verifiable tasks, how much that pushes the performance and generalizes to other domains when we don't have automated verification.

**34:43** · Like, can we generally make the model smarter and smarter in areas that we can verify and minimize or remove the need for labeled data in on non-verifiable domains based on that?

**35:01** · So I think that would be an interesting research area, of course, a very compute-heavy research experiment.

**35:11** · There are some questions that people are asking-- what are some other applications of AI that don't fall into verifiable problems?

**35:21** · So it comes in-- I can just think about some areas that verification is very slow, like scientific discovery, running a very slow simulation in chip design that takes like a few days to run to collect one kind of reward signal, or running this chemical experiment that you actually need to go to a vet lab and run things and see what the output, the quality or the reward is.

**35:53** · Those are the domains that the verification is really hard because in RL fine-tuning, or in test-time scaling, we need these verifiers to be almost instant, or we can wait a little bit.

**36:07** · Maybe we can wait minutes.

**36:08** · Maybe we can allow one hour.

**36:11** · But if in this RL training route-- RL training, we need like hundreds or thousands of steps of iteration, we can't wait like days or someone human in the loop to collect the reward for us.

**36:27** · So those are the non-verifiable domains-- those are some examples of non non-verifiable domains.

**36:35** · I think truly non-verifiable also comes from creativity or any metrics where there's subjectivity in some ways.

**36:44** · Like creative writing, it's like designing an exact reward function for that is hard.

**36:52** · But of course, we can always model that.

**36:54** · But then you can-- the RL or the agent can do reward hacking if the model is slightly off base.

**37:04** · Any other questions from the class on this aspects?

**37:11** · Yeah, we have one question.

**37:12** · Can you hear us?

**37:13** · Yes, we can hear you.

**37:17** · You mentioned the harder areas to verify, like how are people attempting to sort that?

**37:28** · For example, like chip design or bio disturbance?

**37:37** · So one way to go about it is to train a model, like a separate reward model that can predict the outcome of a simulation.

**37:49** · So instead of actually running those expensive simulations or emulations or through experiment, you collect a lot of data on them offline, and then you train a reward model that for a given input, it can predict the quality of the output and you use this reward model as your verification object, like in the loop of RL optimization and so on.

**38:16** · But of course, the generality of the reward model is a function of how much data you have.

**38:21** · And it can be inaccurate and that can cause problems.

**38:28** · So that's one area.

**38:30** · Akanksha, do you have any?

**38:32** · So I think we talked about chip design and so on.

**38:35** · But even before going to chip design, just the kernel bench stuff that was done at Stanford in your lab, even there, for example you get compiler execution.

**38:46** · So you can see that, did you generate the right code or not?

**38:49** · You can get some metrics.

**38:50** · But there's a class project that is actually trying to read performance profiles as you make things more complex.

**38:56** · And that's a harder problem.

**38:59** · And so you basically, even though you might be able to do design-optimized kernels for simple enough things, but if you actually concatenate all of these things together and you want to performance profile and change parts of the code that are not optimized, that's a harder problem in some ways.

**39:17** · And oftentimes the way people will go about solving it is OK, the models can solve maybe the kernel optimization problem.

**39:25** · So maybe I break down the problem into subparts and then get the model to look at each part and then have some reference solutions to look at a knowledge base.

**39:35** · I'm literally describing A class project right now.

**39:37** · So what I'm trying to say here is that because of this being a hard-enough problem, and the models not being at that capability, often it requires breaking down the problem in interesting ways to what the models are able to do now.

**39:59** · Let's move to a more along the lines of, OK, we can do the self-improvement.

**40:04** · But you're now doing a lot more inference.

**40:07** · And there's a cost to this intelligence.

**40:10** · So Azalea will cover more on how to get efficiency there.

**40:14** · Sounds good.

**40:15** · Should I present myself or would you scroll?

**40:19** · Like what would-- Whatever is fastest, I can continue to.

**40:23** · If you just tell me next, I'll continue.

**40:25** · OK, sounds good.

**40:26** · So next, please.

**40:28** · So this is a recent work that we did in collaboration with Professor Ray and Professor John Hennessy and a large team of great collaborators.

**40:42** · So in this project, what we are looking for is like looking into the trends that are happening on the model side and also on the hardware accelerator side.

**40:54** · And what we are interested in thinking about the future and thinking about how the workloads and AI inference is going to look like in terms of the type of the size of the models and the type of accelerators that we are going to need to serve them.

**41:16** · Next please.

**41:20** · So right now, we are in the mainframe era, meaning that the LLMs that we are running are using ChatGPT, Gemini.

**41:35** · A lot of these larger models that we are running, all of them are being run on cloud.

**41:42** · We don't run them locally because these models are large.

**41:46** · Some of them we even don't have access to them.

**41:48** · They're proprietary and even the open source fund for the larger models, we are still using cloud to run these models.

**41:55** · And at the same time, what the observation is that the demand for compute as a result is exploding.

**42:03** · Like Google Cloud grew in something in the order of 1200x in the last 20 months in terms of the compute serving.

**42:13** · NVIDIA had a 10x year-over-year kind of growth.

**42:18** · And this is crazy.

**42:20** · These numbers are explicitly driven by AI.

**42:25** · And as a result, we are going to need something in the order of 250 gigawatt of data centers to be able to serve this demand right now.

**42:35** · And again, this is exploding.

**42:37** · So that means you're going to need more and more energy kind of supply for these data centers.

**42:45** · On the right side, we're showing this graph of the number of tokens that are kind of from on the Google side has been processed.

**42:56** · So in the February of last year, it was 160 trillion.

**43:00** · And in October of this year, it was 1.3 billion.

**43:06** · So this is one of the fastest growing compute demands that we are seeing in history.

**43:12** · Next, please.

**43:15** · At the same time-- so we looked into what kind of workloads are, or the type of activities or AI serving demand that we are observing.

**43:26** · And then from this data set, this very large-scale data set of ChatGPT users, it turns out that something in the order of 77% of requests are for task like practical guidance, information-- like asking for information or writing.

**43:47** · And a lot of these tasks, it turns out that we don't need the very best frontier models to answer them correctly, rather smaller and local models can be used to address them.

**44:03** · So on the right side, you're seeing this kind of categories of user queries, the type of user queries that exist over time.

**44:13** · And what is interesting here is that, of course, users are going to ask more and more complex problems from the chatbots over time because the chatbots are getting better.

**44:24** · But still, it's kind of like the vast majority of the type of queries that are being asked are on the side of, again, the simpler side of complexity that can be addressed by smaller models rather than large proprietary models.

**44:44** · Next, please.

**44:48** · Another trend that is happening right now is the improvements in local inference accelerators.

**44:56** · So the graph on the right, what it shows is that since 2012 up until now, we saw something like 126x improvement in the GPU memory of the local accelerators.

**45:11** · And right now, we have laptops that-- our MacBooks could have something in the order of 100 gigabyte of memory.

**45:20** · And that means that we can fit very, very large model, especially if we serve the model in quantized versions like into it.

**45:30** · And so the larger some of the largest models that are out there, we can take them and serve them locally, which is a very interesting trend that is following this other trend that a lot of user queries are addressable by smaller models.

**45:48** · Next, please.

**45:50** · So the question that we wanted to answer here is that, what role can local inference play in redistributing the inference demand?

**46:02** · So we have all this traffic right now that pretty much all of it is going to cloud.

**46:08** · Pretty much all of it is going to these accelerators like H100s and TPUs and GP200 and GP300s.

**46:17** · But the trends right now are suggesting that maybe we can do something different here.

**46:23** · And so let's see the next slide.

**46:27** · So in order to look into this more systematically, we first define this new metric that looks into not only the capability or the way the models are-- the accuracy of the models, but also on the efficiency side.

**46:45** · So on the capability side, we are looking this metric that I'm about to define called intelligence per watt, is looking into the percentage of the queries that are addressable by the model for the single turn and reasoning type of queries.

**47:07** · And when I say local models right now, at least in this study, we considered those are the models that have 20 billion active parameters or less.

**47:19** · And on the efficiency side is how much useful compute we can get from these per watt from running these models on our local hardware.

**47:30** · So in short, the definition of intelligence per watt is the average task accuracy divided by the average power draw to solve this task by the model.

**47:43** · Next, please.

**47:46** · And we looked into a variety of models hardware workflow type of tasks and evaluation metrics.

**47:54** · We looked into more than 20 local models like Qwen, GPT-OSS, Gemma3 and so on.

**48:02** · We looked into both enterprise accelerators and local accelerators.

**48:08** · The type of workloads we looked into, as you can see here, there were 1 million queries from source from ChatGPT and other reasoning benchmarks such as natural reasoning, MLU pro and super GPQA.

**48:24** · And we also looked into the evaluation metrics such as accuracy, energy latency, the compute used and so on.

**48:32** · And all of these data-- so this massive data, we used it to understand the trends, but we are also open-sourcing all of these kind of different metrics across different type of underlying model and hardware sub-trees.

**48:49** · Next, please.

**48:51** · So here is our findings.

**48:54** · It turns out that local models not only are very, very good already, but the trend of their improvement is also very interesting.

**49:05** · So since 2023, there was a 3.1x improvement in the accuracy or the portion of the chat queries that they could solve.

**49:19** · This is very, very fast.

**49:21** · And this happened in only two years.

**49:24** · And right now, among the queries that I described in the previous slide, they could address something in the order of 88.7% of all these queries.

**49:35** · This is a very, very large number.

**49:38** · Another observation, which is kind of not very surprising, is that local accelerators, in terms of their efficiency, they lag behind enterprise chips.

**49:50** · For example, an Apple M4 Max, it delivers 1 and 1/2x lower intelligence per watt than the B200.

**50:03** · And the reason for that is that these B200s are extremely optimized to run language model workloads, whereas an Apple M4 of course, is optimized to run these AI metrics, but there are other kind of workloads that are out there that they're optimized for.

**50:21** · And in general, while designing these chips, the understanding wasn't that the LLMs are going to be running locally.

**50:31** · That's why the majority of focus of chip designers are on this cloud scale chips for running these workloads.

**50:40** · And lastly, there's this other very important observation that the intelligence efficiency, or the improvement in this metric is something in the order of 5.3x over the last two years.

**50:55** · So 3.1x of it is coming from better models.

**50:59** · Another 1.7x of it is coming from the improvement in the hardware and how the hardware is becoming more and more efficient.

**51:07** · So both of these-- so both of these trends, one, is that local models are becoming better and better.

**51:17** · They can solve problems that they couldn't solve before at this very accelerated rate.

**51:25** · At the same time, model efficiency is becoming better and hardware efficiency is becoming better.

**51:32** · This suggests that we are heading towards this future, that more and more of this traffic can be addressed, or can be solved by models that we can run on our edge device, for example, on our laptop or on our phone device in the future.

**51:49** · Next, please.

**51:53** · So let's go the next slide.

**51:58** · So with that, I get back to the IPW and the future directions for that in a second.

**52:06** · But given this observation and everything else that we have learned in this class, there are a few directions that remain open.

**52:17** · There are a lot of interesting research questions around it that are not addressed yet, and it's going to be interesting to work on.

**52:25** · One is the foundational principles in test time scaling and learning from this like new kind of era of synthetic data and synthetic data flywheel that these models are creating.

**52:40** · Right now, the way we are approaching it is through RL, through collecting this data and then fine-tuning the models.

**52:48** · But it kind of like suggests that there is more here, our understanding of, first of all, why are we seeing this kind of property?

**53:01** · What does it suggest from the model that as we ask the model a question over and over again through test time scaling, what is happening that these correct answers are coming out?

**53:11** · What are the best practices to distill this successful trajectories back to the model?

**53:19** · These are still open questions.

**53:21** · And there is a very clear segue from this synthetic data flywheel kind of phenomenon, back to continual learning.

**53:31** · Something that seems like maybe it's not really we haven't gotten it right yet, is the following-- like us humans, as we solve tasks, as we solve problems and study and do new things, there's this continual kind of progress in how our brain develops and how we become more and more skillful.

**53:54** · Whereas for the models, it seems like mostly there's this offline process of here is like some agent take up kind of experiences that are generated.

**54:05** · And then maybe after some time, there's this fine-tuning process of the model.

**54:12** · It is not something that happens on the go.

**54:16** · And there is this kind of a mismatch between human behavior and model behavior that a concept like continual learning could potentially add answer.

**54:27** · Like, what are the new practices that we can bring in model development that we can bring these positive experiences and learning from negative experiences and problem solving that the model do back into the model in a more natural way that is different from the current asynchronous, like data generation and fine-tuning paradigm?

**54:57** · The last piece is the infra for the high throughput, low latency test-time scaling.

**55:04** · So again, the way we do test-time scaling, but there is repeated sampling, whether it's these kind of back and forth in terms of updates that we do to the previous generations.

**55:20** · We do tool calling.

**55:21** · We do this and that.

**55:22** · That is very different from the current mainstream chatbot usage, which is just mostly single turn back and forth with the model.

**55:33** · And what that means is that there are a lot of opportunities for doing systems and inference optimization work for these type of test scaling.

**55:46** · My lab did some of this work, like works like hydrogen token SRS.

**55:51** · And these things are going to matter again a lot more in the future because these methods are becoming more and more mainstream.

**55:59** · So that means we need to have specific ways to deal or optimize the systems and the underlying compute for them.

**56:07** · So overall, it seems like pre-training-- looking at this figure on the bottom of the slide, pre-training a lot of interesting work in their discourse or our series of lectures touched less on that, even though Akanksha is an expert on pre-training.

**56:25** · But we mostly focused on post training and the test-time scaling methods.

**56:31** · And there is this new kind of unleashed era of like synthetic data, flywheel, and continual learning that is happening in this kind of connection between the fine-tuning and online learning and test-time scaling that we hope that all of you learned a ton about it.

**56:50** · But there's also a lot of interesting unsolved challenges that you can address going forward.

**56:55** · Next slide, please.

**57:00** · Going back to the IPW metric and the observation about the shift, the possible shift from everything on cloud to a lot more locally also suggests new direction in terms of inference serving engines that are hybrid, that we can smoothly route traffic between our local and cloud kind of models and accelerators, depending on the need and the complexity of the resources.

**57:36** · The other direction here, again, is new model architectures and kernels that we can use for energy efficient inference, especially on the local accelerators that we have, which this is like area that is much less kind of focused on compared to the cloud accelerators.

**57:58** · And the other important piece is that energy is going to be the most kind of valuable resource that we have going forward.

**58:07** · And metrics such as intelligence per watt and better ways of our understanding of measuring energy and watt and power usage and optimizing for that, again, is going to be very, very important.

**58:22** · And that is an area that is less worked on right now in terms of the target metric of optimization.

**58:33** · But we expect that it becomes more mainstream and more popular going forward.

**58:41** · And I think that's the last slide on the future directions.

**58:52** · Akanksha, you are muted.

**58:58** · There are some things in chat so.

**59:03** · I'll start with the first question here.

**59:05** · Do you think this is more pertaining to memory systems or the alarms themselves?

**59:15** · I'm guessing-- so whoever asked this question, can you ask it real time perhaps to put a little bit more context there.

**59:22** · Otherwise we're guessing the question.

**59:25** · Yeah, happy to.

**59:28** · Yeah, I was just referring to a few slides back when you were talking about that continual learning from failures and success.

**59:38** · Do you think that we're going to see more of that in long-term memory systems and architectures or what's designed around an LLM or the models themselves, in terms of what's improved and what's worked on?

**59:54** · So I think the continual learning idea that might pertain to long term-memory systems, that would be the human analog of it.

**1:00:02** · But if you're trying to-- but before we even go there, even in multi-step reasoning, learning from success or failures or getting the model to keep that skill set and update things in the weights, or in subset of weights in a useful way, can you learn a new skill?

**1:00:23** · Learn how to learn is an important capability that we basically don't have right now.

**1:00:30** · If you can watch videos, robots, try this.

**1:00:33** · When can you watch videos of how to do something and learn how to do it, as opposed to being given a lot of task demonstrations.

**1:00:45** · Azalea, do you have more to add there?

**1:00:49** · You're muted, if you're-- Yeah, I think there are other ways also to bring this knowledge, like obviously in context learning is one way to enable continual learning.

**1:01:07** · One way I think about is imagine we had an infinite context that the model could perfectly have access to every piece of it and could learn from everything in it.

**1:01:19** · We don't have that.

**1:01:20** · But if we had that, maybe that was one solution to continual learning.

**1:01:26** · Because we could put everything positive and negative in the context, and the model could just remember all of that at the same time and reason over all of that at the same time.

**1:01:35** · But we don't have that.

**1:01:37** · And we go through right now, even a million or a few million models capability to reason over its EICL or in in-context kind of data diminishes.

**1:01:52** · And there are other ways that we learned about cartridges in the span of our lectures.

**1:01:59** · So that's one other way that we are enabling this long context and in context learning without changing the weights of the model, without fine-tuning the model, but instead bringing them into the activations, or in this case into the KB caches of the model.

**1:02:18** · So all I'm saying here is that there are other ways to think about continual learning without model fine-tuning, one could be by just increasing the effective context length massively.

**1:02:37** · And that could be another approach to long-term memory and continual learning.

**1:02:48** · As a follow-up to that, in practice, like in implementation, do you think, what would be easier to do?

**1:02:57** · Constantly, updating the model's weights or updating a memory store?

**1:03:03** · I think it depends on the application.

**1:03:05** · I mean, of course, you can argue that updating the memory store would be easier.

**1:03:13** · If it's a knowledge base, if what you're-- I mean, the simplest, my version of that is that if I could keep a database that the LLM could learn to look at, then I should just go update the database.

**1:03:24** · But what you're really trying to teach the LLM is to the ability to reason over new domains.

**1:03:30** · And oftentimes having a side memory system doesn't quite achieve that.

**1:03:34** · So that's where updating the weights does the job better.

**1:03:37** · And the example that I was giving in robotics actually is very pertinent there as to no matter how much memory systems you add, the robot which has learned-- I mean, the cross embodiment generalization that you were looking at on the lecture on Monday, for example, that doesn't happen if you don't update the weights just by having memory systems.

**1:04:00** · So that's more of a skills transfer problem.

**1:04:04** · Makes sense, yeah.

**1:04:05** · Thanks so much.

**1:04:09** · There's one more question, I think from-- what he's saying is that in the absolute zero paper, the environment seems like the data used for post-training.

**1:04:19** · Is there a paper for agents to self create environments?

**1:04:25** · I mean, if you go back to the worlds where there was narrow intelligence, there you could basically create simulations for games.

**1:04:35** · And those were used as environments for toy tasks.

**1:04:41** · The reason environments matter in the current generation are that they are proxies for real-world tasks.

**1:04:47** · So it's not so much that there's a paper for agents to self-create environments.

**1:04:51** · It's more along the lines of what is the set of tasks that you're trying to represent.

**1:04:55** · And if there is an easy way to simulate them, then whether you use agents to create that or software to create that, that's fairly straightforward.

**1:05:04** · But is it a reasonable proxy of how the model will interact with the real world to get feedback.

**1:05:10** · And for gaming, it's kind of a finite space to explore.

**1:05:17** · So it's easier to represent that in code and have simulations.

**1:05:23** · OK, thank you.

**1:05:26** · More questions from the class?

**1:05:41** · You were saying something?

**1:05:42** · I think up here is a question.

**1:05:46** · We can't hear you because you have to speak up.

**1:05:48** · I think that there are no further questions.

**1:05:52** · OK, awesome.

**1:05:53** · OK, cool.

**1:05:55** · OK, so let's start by-- let's end by thanking the class.

**1:05:59** · It's been a real pleasure teaching you all and creating the content for this class so that you can learn about the latest and greatest set of techniques in the self-improving agents area.

**1:06:12** · It's a evolving area, so anything that we teach now starts to be history by the next time the class rolls around.

**1:06:20** · And yet the basic techniques that you're learning are extremely valuable over time, because a lot of the new stuff still builds on top of the basic techniques.

**1:06:33** · So really grateful to have worked with you all and looking forward to what you do in your projects and your posters.

**1:06:40** · I'll let Azalea also thank the class.

**1:06:43** · Yes, thank you so much for-- the way we created this class is that we were also learning about a lot of things as we were creating the slides and we were preparing the course material, because a lot of these topics are just like so fresh and so new.

**1:07:03** · And we were excited about them and we wanted you to also be aware of them.

**1:07:07** · So thanks for accompanying us in this journey.

**1:07:12** · And we are very grateful to you and we hope that you learned some new skills, you got inspired in some new directions, and we really hope that this is just the beginning for you to go ahead and do so many more amazing work in your research projects, in your jobs, and in the future in general.

**1:07:34** · So thank you so much.
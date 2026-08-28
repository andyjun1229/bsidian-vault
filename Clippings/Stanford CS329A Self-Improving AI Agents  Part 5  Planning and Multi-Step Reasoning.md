---
title: "Stanford CS329A Self-Improving AI Agents | Part 5 | Planning and Multi-Step Reasoning"
source: "https://www.youtube.com/watch?v=Ml_fp9XkB8Y&list=PLangBM27OtEA&index=5"
author:
  - "[[Stanford Online]]"
published: 2026-08-03
created: 2026-08-26
description: "Want to dive deeper? This curriculum is covered in the following online courses:- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html- XCS329 graduate course:"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=Ml_fp9XkB8Y)

Want to dive deeper? This curriculum is covered in the following online courses:  
\- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html  
\- XCS329 graduate course: https://online.stanford.edu/courses/cs329a-self-improving-ai-agents  
  
A similar curriculum is covered in XCS329z https://online.stanford.edu/courses/cs329z-engineering-ai-agents  
  
Follow along with the course schedule and syllabus: https://cs329a.stanford.edu/  
  
View the course playlist: https://www.youtube.com/playlist?list=PLangBM27OtEA  
  
Video Summary:  
This lecture video from Stanford's CS329A, Self-Improving AI Agents, taught by Azalia Mirhoseini on October 6, 2025, covers three papers on planning and multi-step reasoning in language model agents. LATS, or Language Agent Tree Search, combines reasoning, acting, and search using Monte Carlo Tree Search with LLM-judge and self-consistency scoring, tested on HotpotQA and WebShop. SPRINT fine-tunes reasoning models such as DeepSeek-R1 to generate independent plans for parallel execution, reducing sequential token count while improving accuracy on math, Countdown, and GPQA Diamond benchmarks. SWiRL generates offline synthetic multi-step tool-use trajectories scored by an LLM judge and trains models through multi-step reinforcement learning without executing tools during training, showing generalization across HotpotQA and GSM8K. The lecture addresses trade-offs including inference cost, irreversible actions, and the comparative effect of process-filtered versus outcome-filtered training data.  
  
Speaker Bio:  
Azalia Mirhoseini  
Assistant Professor of Computer Science, Stanford University  
  
Azalia Mirhoseini is a co-founder of Ricursive Intelligence, a frontier lab dedicated to recursive self-improvement through AI that designs the chips that fuel it. She is also an Assistant Professor of Computer Science at Stanford University where she directs Scaling Intelligence, a lab focused on developing scalable and self-improving AI systems and methodologies toward the goal of artificial general intelligence. Previously, she spent several years in industry AI labs, including Google Brain, Anthropic, and Google DeepMind, working on the development of Claude and Gemini. Her past work includes Mixture-of-Experts (MoE) neural architectures, now predominantly used in leading generative AI models; AlphaChip, a pioneering work on deep reinforcement learning for layout optimization used in the design of advanced chips like Google AI accelerators (TPUs) and data center CPUs; as well as pioneering research on LLM Test-Time Scaling. Her work has been recognized through the Okawa Research Grant, the Google ML and Systems Junior Faculty Award, MIT Technology Review's 35 Under 35 Award, the Best ECE Thesis Award at Rice University, publications in flagship venues such as Nature, and coverage by various media outlets, including WSJ, NYT, Forbes, MIT Technology Review, IEEE Spectrum, WIRED, and TechCrunch.

## Transcript

**0:05** · So today's lecture is going to be about planning and multi-step reasoning.

**0:11** · So today's lecture, we are going to cover three papers on multi-step reasoning and planning.

**0:17** · Let's start with this paper from ICML of last year.

**0:26** · So the title of the paper is Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models.

**0:37** · So the types of applications that we want to target in multi-step tasks are tasks that we not only need to reason about things, but also need to act through those reasoning steps and search our trajectories, or optimize trajectories and how we get to a final correct answer.

**1:02** · So in the reasoning step, the model needs to think about what needs to be done?

**1:08** · For example, what the budget is, where the plan is.

**1:11** · These are the reasoning steps for a trip or vacation planning prompt.

**1:17** · The act is OK.

**1:19** · Now that you have certain types of reasoning or thinking, how do you gather more information, or act on these reasoning steps?

**1:28** · For example, the action could be a browsing the web, generating a query to search, read Reddit, or a travel blog, and so on.

**1:40** · And then another step is search.

**1:45** · Given these feedback, or the information that's gathered online, how can we refine our plan so far?

**1:55** · Maybe we can consider alternative destinations, search new things to do while we are there, and so on.

**2:02** · So there are a series of reasoning, action, and search steps that needs to be done to solve this problem of, for example, planning a trip.

**2:13** · So the problem, or the challenge that this paper specifically wanted to address was the following.

**2:23** · The goal here was, let's go from the LLM, generate a plan, and executing on that plan, to really try to encourage diversification and exploration of different types of plans, or paths that the model can take because models-- And this is true still to this day, that creating a diversity of solutions, or acting upon them and planning multiple steps of optimization to reach a solution.

**2:58** · So this paper focused on bringing known techniques from reinforcement learning and multi-step planning that existed in the past, including multi-step Monte Carlo tree search into the LLM reasoning path.

**3:16** · And given that the models can take feedback in, it also introduced ways for the model to take different feedback as the model explores with the environment and bring that back in order to refine and optimize future plans and search processes.

**3:39** · So just a quick example of how this worked.

**3:47** · For example, the prompt is to plan a trip to Hawaii.

**3:51** · There are different ways and different actions that the model can take, so it can, for example, if we sample the model for this prompt, the model might decide that we might consider asking friends that already went to Hawaii, or read subreddits related to that.

**4:13** · And then this framework introduced a mechanism for getting a score for each of these actions, and then update the search space, or the trajectory of follow-up expansion of this tree that is being formed based on that score.

**4:33** · And we talk about how these scores are generated.

**4:36** · In this case, action 1 has a higher score, so we expand that action, so the model expands that action.

**4:44** · So in this case, ask two friends, friend a and friend b, about opinions, and then based on the quality of responses, their score for that, and the model can expand from there, so there is a flavor of multi-action sampling in this case.

**5:06** · The actions can, in fact, be executed in parallel.

**5:09** · Like these two actions, or these two actions, they both can be executed in parallel.

**5:15** · And there's this notion of let's do continuous exploration based on the best state, but also consider a mix of exploration and exploitation, and that's where the MCTS comes in.

**5:33** · So there are two papers that-- this paper was basically saying, how it diverges from those.

**5:41** · Math-Shepherd is a paper that we saw previously, and in that paper, there was a verifier that was guiding the search process in the test time.

**5:51** · Basically, the reasoning trajectories are scored by this verifier, and then the expansion is guided by that.

**6:04** · But in LATs, which is this paper that we are going to learn more about in this lecture, this scoring is not based on reasoning theorists, but it's based on the outcomes of the actions that the model takes.

**6:19** · And also there is this part about reflection of the model to evaluate how this trajectory went, and also about the observations from the environment.

**6:32** · It also improves based on previous methods frameworks on reasoning such as the ReAct work, where basically in ReAct, there is this extra step up.

**6:52** · We are going to see how this works, but there is this extra step memorization, and, again, reflection and an interaction with the environment that we have in the LATs paper.

**7:03** · And specifically, we have more and more planning into the process.

**7:11** · So here is the intuition behind LATs.

**7:17** · There is the chain of thought, where the reasoning process is basically decomposed into a number of steps.

**7:26** · There is this notion of tree expansion.

**7:30** · Basically, through these types of actions, that action generation that we have, we have a tree, that we form a tree, and we do search and planning through that.

**7:41** · And then we have this borrowed that from the ReAct framework, where the feedback from these actions are incorporated into this search process for the future search and so on.

**7:57** · So this method concretely has six types of stages, selection, expansion, evaluation, simulation, back propagation, and reflection, so let's see exactly how this method works.

**8:16** · And let's walk through an example prompt.

**8:20** · So in this case, the prompt is navigate through a maze to reach an exit.

**8:27** · And then the initial observation is that you're in a dimly lit room, there are two doors, one on the left and one on the right, and the goal is to reach an exit in this case, so let's see how these different steps of LATs come into play.

**8:44** · So first is the selection process.

**8:46** · In this stage, we need to select a node to expand.

**8:50** · Let's say, we have done that.

**8:51** · We see exactly how that's done, but given that we have selected a node, and this is based on UTC, we are going to see it in a bit, we want to see what actions that we can take from that node.

**9:08** · So in this case, our initialize node is this thing, you're in a dimly lit room and so on.

**9:16** · Now, let's say, the model samples different actions here.

**9:21** · In this case, three actions are sampled.

**9:23** · One is open the left door, open the right door, and the third one is inspect the room for clues.

**9:29** · Then the next step is each of these actions are executed in the environment, and the observation is basically appended to the context.

**9:40** · So in this case, say, if the action is open the left room, the observation is dark corridor with paintings.

**9:48** · Action B is open the right.

**9:50** · There is another observation and so on for action C.

**9:54** · Now comes the evaluation.

**9:57** · So let's say, we have an action, we have executed an action, we want to evaluate our new state that we are going into.

**10:05** · For this part, they suggest averaging for creating a score.

**10:11** · Based on the current action and observation, they suggest adding up two scores together.

**10:19** · One is using an LM score, basically using LLM-as-a-Judge and prompting the model for evaluating how promising this state is, and literally asking it to give a score based on 0 to 1 for this state.

**10:36** · And the other one is the self-consistency score.

**10:39** · And that is, let's assume instead of three actions here, we had sampled 50 times.

**10:48** · We had sampled 50 actions, and we categorized them into different types of actions.

**10:53** · And if an action is sampled more, we give a score corresponding to the rate, or the frequency of an action being sampled.

**11:04** · So in this case, the self-consistency score for state A was higher because 75% of the time maybe the action was sampled, so the way to create just one value for this action is to add up these two.

**11:22** · So now we have a value for action A corresponding to state s\_A.

**11:31** · And then we have the simulation part.

**11:34** · For example, in a greedy method from the previous stage, we have s\_A having the highest score.

**11:41** · s\_B and s\_C have much lower scores, so we go and expand s\_A all the way begin.

**11:49** · We can continue this process.

**11:50** · We sample more from s\_A and we continue expansions until we reach an end state, or whether it's successful, or it fails, or until we reach the budget that we have for expansion of this state.

**12:07** · So in this case, from state s\_A-- so this was s\_A, and then we have the candidate actions that start from that state.

**12:18** · And then in this case, it's greedy.

**12:20** · It takes one action approach, this staircase, and then we reach an observation, which we are lucky in this case, we have the exit door clearly marked.

**12:34** · We got a point here.

**12:38** · And then let's say the simulation is done.

**12:43** · We either have a successful trajectory or it's a failure, then we can-- the important part here is how do we use this observation to backprop and update the scores that we had for different actions that were taken?

**13:00** · So this is the backprop stage, and then that is used to influence the score of each state, and we're going to talk about it in a bit.

**13:11** · Let's talk about how these value function and backpropagation is used.

**13:15** · So for the value function, we already saw that.

**13:19** · That is a weighted average of asking an LLM-as-a-Judge given this observation, this action, what are the chances of success?

**13:27** · Give us a score between 0 to 1.

**13:29** · And then there is the self-consistency, which basically we just count how many times a given action is sampled.

**13:38** · Then there is the notion of UCT, or upper confidence bounds applied to trees.

**13:44** · That's something that this basically the number, or score that is used for selection because at each point, we have a range of values that we want to see, which node we go and expand.

**13:59** · So the way UCT works, and this is completely borrowed from the MCTS literature.

**14:08** · The way it's designed is to try to balance between exploration and exploitation.

**14:13** · If we just go based on the highest value at that point, we might miss out other nodes that right now, maybe at the current moment have a lower value, but down the road at the end might have higher value, so let's balance the two of them.

**14:29** · So the way UCT works is that it has this exploitation one, which is V of s, plus a hyperparameter, times this other term, which encourages exploration.

**14:41** · And the way this work here is that the Np is the number of times a parent of a node is visited, and Ns is the number of nodes that this current node is, not the parent, but the current node is visited.

**14:54** · And basically, think about it this way.

**14:57** · Relative to the parent node, if a node is visited less, we want to encourage visiting that node more.

**15:04** · And if that node relative to the parent is visited a large number of times, then this number, this division, this becomes a smaller number and UCT becomes lower relative to unexplored children of a parent node.

**15:24** · So UCT, again, is the number that we use for selection of a node and going from there.

**15:32** · Now, back propagation, and that's where we go at the end of a trajectory, either we succeed or fail.

**15:40** · The return of that trajectory is used to update the values, and this is like back propagated through the steps.

**15:47** · So at each point, the value of a state is the value of the old state, times the number of visits to that node, minus 1, plus the return, divided by the total number of visits to that node.

**16:02** · So that's how the math behind this framework.

**16:07** · Yes.

**16:09** · Why does it have one \[INAUDIBLE\] you take a long time, but it didn't take long?

**16:19** · It's just something.

**16:20** · There's some math and theoretical intuitions behind it.

**16:24** · There is no proof that this is the optimal round, but you want to just balance the two in that this is considered a more optimized way of doing things.

**16:35** · \[INAUDIBLE\] Yes.

**16:43** · So once backpropagation is done, they also append this reflection of the model itself about the trajectory that was expanded.

**16:56** · If it fails or it succeeds, the model adds some thinking behind what happened, what led to the failure or the success of this trajectory, and this apparently has been very helpful in overall increasing the quality of this approach.

**17:14** · So they tested this approach on HotPotQA, which is some data set that we use it for multi-step reasoning optimization.

**17:24** · Basically, the way this data set works is that for each question for answering them, you need retrieval from, at least, two different Wikipedia pages because it's just designed like that, so you need this multi-step by design process in order to find an answer.

**17:42** · And they're doing really well.

**17:46** · Just look into in terms of as they increase the number of samples or the number of trajectories that they sample, they can significantly improve performance, and the reflection and bringing those reasoning traces also gives a lot of boost at the end to the model.

**18:06** · So basically, they have provided a mechanism to translate more compute at test time effectively to better solutions for this multi-step reasoning tasks.

**18:19** · They also tested that on WebShop, which is this interesting data set for practical applications.

**18:33** · This is just to show you an example of how this data set works.

**18:37** · For example, there is-- I'm looking for a small portable folding desk that's already fully assembled.

**18:43** · It should have this color and this finish and so on, and the price is-- so it's by design, it's a multi-step process, and they're showing that their approach without any fine tuning.

**18:57** · And just at test time, they can get really high results, even close to human experts in this case.

**19:09** · So to summarize, what LATs proposed was a new technique for bringing in reasoning, taking actions and planning all together, and brought in our known ideas like MCTS into the language model world.

**19:27** · And they got very strong results on multiple domains.

**19:31** · And given their test time approach and the modular approach, it's very portable and relatively easy to create.

**19:42** · The downside, of course, is the cost.

**19:47** · Each of these back propagation and expansion of a tree, all of those are adding a lot of cost, and the cost benefits was not really analyzed in the paper.

**20:00** · Another assumption that this paper didn't address was really that there are scenarios, where taking an action may be irreversible.

**20:10** · So that's going to be challenging like, how do we adapt to those scenarios, if, for example, the model is running a transaction?

**20:19** · If it actually takes those actions, it could be very consequential, like paying for a service and so on.

**20:25** · So that is another scenario, where this approach might not be adaptable to.

**20:35** · So here, there are a few questions about this paper that I really would like you to think about it maybe for a couple of minutes, and then we discuss anything related to where you see the strengths or weaknesses of this paper, or if you were to adapt it or extend it, how would you do that?

**20:55** · So let's start doing that, and I'll get back to you in a couple of minutes.

**21:03** · All right, let's get back.

**21:05** · Anyone wants to comment on this fork?

**21:09** · So the UCT method is basically like upper confidence-bound from banded learning setting, right?

**21:16** · There's other algorithms for embedded learning like picking and exploring various arms.

**21:22** · Did they try different ones in this paper?

**21:26** · The question is UCT is one way to create this exploitation, but there are a lot of literature, now that whether they compared?

**21:35** · Yeah.

**21:36** · No, and there is that whole literature of multi-armed bounded and other ways that we can bring in exploration, exploitation into the optimization process, and all of that could be also explored here.

**21:51** · Their main contribution is that created a platform that now others can bring in other approaches to optimization.

**22:01** · Yeah.

**22:02** · Anything else?

**22:05** · Questions or comments?

**22:11** · OK, let's move on to the next paper.

**22:15** · \[INAUDIBLE\] Yes, go ahead.

**22:19** · If we want to keep track of the action trajectory based with the Monte Carlo tree search, what if there are times when there's repeated actions like action AB, AB is, or when the same action is seen in multiple nodes, is there any way to optimize this tree, or does this tree recognize all of these repeated actions as independent trajectories?

**22:49** · So the question is, if a series of actions are repeated, how do you-- so the philosophy behind this is that if an action is repeated inside a trajectory, given a parent node, you would increase the count of that action, and that comes in the UCT formulation.

**23:11** · So ideally, you would capture in that as you are forming this tree.

**23:17** · And ideally, this is a tree that you're forming.

**23:20** · Not some fully connected graph, so this is the assumption behind this.

**23:26** · Yes.

**23:29** · So let's now talk about SPRINT.

**23:32** · This is a NeurIPS 2025 paper, so this hasn't been even presented here at the conference.

**23:39** · So this paper is about, again, it gives you a flavor of this planning and parallel execution of those plans and how we can use the model itself to enable it to think better in parallel, and we can optimize that.

**23:59** · So this paper, SPRINT, was motivated by this observation that the reasoning models such as o1, Gemini Think, Gemini 2.5 Pro, and pretty much all the frontier models right now, they have this tendency that for harder problems, they think more.

**24:22** · And this longer thinking corresponds to higher accuracy, so these models to think for longer and longer like chain-of-thoughts.

**24:32** · For example, these two graphs here show that the DeepSeek-R1 during the training process.

**24:38** · As the training process continues, obviously, it becomes better at solving this, Amy, these math problems.

**24:46** · But also, if we take a look at the average length per response, that is also going up, so it seems like there is a correlation between model thinking for longer and a larger sum of number of tokens and the accuracy that we get from that.

**25:01** · Now, again, so the observation here was that these long reasoning steps are helpful, but at the same time, many of these reasoning steps seem to be independent of each other.

**25:18** · For example, the model tries alternative approaches, it decomposes a task into subtasks that some of them can be run in parallel, and then some of these steps are verifying the previous steps.

**25:31** · But there is a lot of-- if we look into the graph that describes the reasoning trace, there are parts of these computations that are independent of each other, so we don't need to really wait for all of these steps to be created sequentially by the model, so we want to see how we can leverage this parallelism observation.

**25:57** · And so the idea is, we want the model identify this parallelization opportunities and act on it.

**26:05** · So SPRINT is a framework that does come in during the post-training and/or fine tuning process, and what it does is that it takes a reasoning model and enables the reasoning model to execute the response generation.

**26:25** · We are a planner that creates a set of plans for how to approach solving a problem and a set of executors, and those executors can be run in parallel in order to carry out the plan.

**26:45** · And this can happen again and again.

**26:47** · We can have the next slide.

**26:48** · We can have a plan, a bunch of execution plans that are carried out in parallel, and then we can have another set of plans and then another set of parallel executions, so the interleaving of these planning and execution is what it can enable acceleration of the reasoning process.

**27:13** · So let's see how we can enable the model to create these parallel traces.

**27:22** · And this is something that I want you to think about it beyond just this paper, and we're seeing it in the following work that we are talking about.

**27:30** · A lot of times when we want to create data and figure out a certain behavior in the model, we can use the LLMs itself in the fine tuning data creation process, and here is an example of that.

**27:48** · Given a reasoning model's response trajectory to a question, we can decompose it in a number of steps via an LLM.

**28:00** · So in this case, for example, we had DeepSeek-R1 generate these reasoning traces and responses to these questions.

**28:08** · And then we had a model like GPT-4o going through this reasoning trace, and annotate the steps of the reasoning response.

**28:19** · And not only that, for each of these steps, we ask the GPT-4o to annotate whether which part is the planning part, and which part is the execution part.

**28:32** · And in some steps, there were multiple execution pieces for a given plan.

**28:40** · So for example, we had this query, we had the reasoning trace, and then there are a bunch of things that needs to be done.

**28:47** · And then when the reasoning stops, there is a final answer.

**28:52** · Then we use GPT-4o to go through this process and create these steps 1, 2, and k.

**29:00** · Basically, now we have these annotations, and within each step, the model also annotates the plan and the execution.

**29:09** · Which part is the planning part?

**29:11** · Which part is the execution of that plan?

**29:15** · Given that, then we can create a DAG of these steps.

**29:21** · So we have step 1 and step 2 and all the way, and we can, again, use the model.

**29:26** · And the model does a really good job here of saying whether how these steps are related to each other.

**29:32** · For example, step 4 and 2 are not dependent on each other, but they both depend on step 1-- is a follow-up to step 1, so now we have a DAG of an optimizer and basically, creating the DAG that describes how this reasoning trace works.

**29:52** · And then we can do packing of these steps.

**29:55** · For example, step 1 can be done first, and step 2 and 3 can be done completely in parallel with each other and so on.

**30:03** · And once we have these data set that we have annotated, then LRM here is just a large reasoning model.

**30:14** · Basically, all LLMs are now inherently reasoning models, so what we are creating here is this data set of the steps, plan, and executions in parallel, and we basically fine tune the model, for example, DeepSeek-R1 to now think in that way.

**30:33** · So previously, we would just create those inherently have these properties, but now we want the model to think more and more in parallel by showing these parallel-like planning and execution traces.

**30:49** · And we just fine tune the model.

**30:50** · In this case, just a supervised fine tuning of basically showing the model the same stuff, the same thinking processes, but now annotated with these texts.

**31:03** · And this helps the model that at inference time, now, the model can output these tags.

**31:10** · For example, here is plan 1, and then here are the execution patterns for this.

**31:17** · And here is plan 2, and so on.

**31:20** · So, for example, for plan i, there is a set of thinking and a parallel execution that the model just outputs itself, and then we can go over executing these plans in parallel, and then syncing the output and returning the context.

**31:36** · And then the model goes through plan i plus 1, and then there is a number of parallel subplans within that the model can output and we can go from there.

**31:53** · Why this matters?

**31:56** · So the cost of LLM inference, especially when we get to multi-step reasoning, becomes a huge burden.

**32:04** · And you might have already noticed that yourself, and you spend a lot of time waiting for the model to output the response it gets.

**32:15** · It might make you not happy, you want the answers fast, but also it's a lot of costs and a lot of delay that goes into generating these responses.

**32:24** · So right now, here is how the sequential reasoning models work, so there is a query, there is a plan, and then execution of that plan.

**32:33** · There's plan 2, execution of plan 2, and so on, so this is the time that it takes to generate, or go over this thinking process and generate the final answer.

**32:44** · But if we could leverage this independence from plan 1 and plan 2, we could have the model execute.

**32:57** · We could have the execution of those plans be done at the same time.

**33:03** · Here is what after we fine tuned with the spring at inference time happens, so instead of model generating plan 1 and executing that, then generating plan 2, model generates these two plans first, plan 1 and 2, and then it starts executing.

**33:21** · The execution of those plans happen at the same time.

**33:24** · And then the execution could be using a tool.

**33:27** · For example, the model is come up with a calculation, and then we can use this calculator Python to execute plan 1 and plan 2 and so on and then go to the next stage.

**33:39** · And the fine tuning data, again, this is another visualization of how given these annotations that we have for plans and execution, we create the fine tuning data, so we are basically asking the model to think in parallel, if the plans are independent of each other.

**33:57** · We are basically teaching the model to come up with plan 1 and 2 at the same time, because they're independent depend of each other and we execute them.

**34:05** · Yes.

**34:06** · So if there's a need for a replaning, how does the model remember which plans correspond to which executions, and all of those things?

**34:18** · Later in the infant stage, after the execution for someone who realizes that, oh, what I did was wrong.

**34:25** · How does it remember to do a replanning of go to the plan of 3 instead of plan of 2?

**34:37** · So this fork, you're bringing the previous work in here.

**34:42** · Here, the model can-- so what we are teaching the model here is that to think about plans at each point of time, even if it's a revision of an existing plan.

**34:57** · If it can generate plans that can be executed in parallel, it should do so.

**35:04** · It should not wait for the execution of plan 1 to generate plan 2, because plan 2 is independent of plan 1 anyway.

**35:13** · So this is how we are creating this data set for training the model to teaching it to think maximally in parallel and generate those plans.

**35:23** · If the model wants to go back and reverse on a plan, it still can do that.

**35:27** · It still sees all of these contexts.

**35:30** · It's just like the model is trained to think more in parallel.

**35:34** · And also because it's trained to be like that, and we have this special tags, or ways of the model generating these plans and execution plans, we can act on it and leverage those parallelism.

**35:48** · Yes.

**35:49** · Is the plan to change the structure of this LLM, because before, you just need to predict the next token, but now you seem to have three parallel lines?

**35:59** · It's always next open.

**36:01** · It's just that there is instead of everything, the plan and execution, one at a time, if there is a tag like here, this is plan i, and here are the execution.

**36:13** · And here is plan 2, plan i and i plus 1.

**36:17** · For example, here is plan 1 and plan plus 2.

**36:19** · This is the high level count.

**36:20** · And then now that we know that there are these two plans, we can just branch out and run them in parallel.

**36:26** · So that's the idea here.

**36:30** · So here is the training recipe starting from-- so we generate 6k thinking trajectories for MATH data set.

**36:41** · We keep the ones with higher parallelization, and we do supervised fine tuning on DeepSeek-R1 Distill-Qwen-7B on this reformatted trajectories.

**36:55** · And the interesting property that we observed was that, so when we started the project, the goal was to maximize parallelism for reducing the sequential token generation, so we save on that.

**37:11** · But it turns out this process actually helps out with accuracy as well.

**37:15** · The model seems to like these more structured way of thinking, and this way of encouraging parallelism helps the model have higher accuracy as well.

**37:27** · And here, what we are showing that is the average number of sequential tokens over the baseline model like R1 Distill-7B.

**37:36** · And the SPRINT model, again, is distilling R1.

**37:39** · This basically, there we are fine tuning the 7B model, and there's a big jump like a 3 and 1/2% jump over that, while also becoming much more efficient than a 32B in terms of number of sequential tokens.

**37:59** · Like you said, there's \[INAUDIBLE\] and more opportunity to explore more approaches given the fixed compute budget, because-- It could be, yeah.

**38:10** · And we have some data on that, which I believe I'm going to show.

**38:14** · The model does explore more and think in parallel more.

**38:20** · And another interesting observation was that we have out of domain generalization as well.

**38:30** · So the training to think in parallel was done for the MATH data set, but we also saw the model is doing better.

**38:42** · Not only have more opportunities for this parallelism, but also higher accuracy, for example, countdown or GPQA diamond data set, so there is no training.

**38:57** · We have not trained on those data sets, but the model generalizes.

**39:00** · And this could go back to what you were suggesting, that the model can think in parallel.

**39:05** · And that inherently seems to help the model, but as a side effect, we also have opportunities for leveraging this parallelism and reducing the number of sequential tokens.

**39:20** · Could there be a scenario, where individually, the answers are correct in parallel branches, but when you combine it, say in a sequential manner, the answer may be wrong, and in that case, what will take precedence?

**39:35** · And in that case-- What will take precedence?

**39:38** · Because sometimes, even in a mathematical equation, individually, when you look at them in isolation, the answer might look seemingly correct, but when you put all the steps together, the answer may eventually be wrong.

**39:53** · So when the model generates, no matter if it generates sequentially, or in parallel, at the end of the day, everything is condensed into the context, so the model sees that.

**40:06** · And this is the thinking process.

**40:08** · The answer, after this, the model should generate a synthesized final answer, so if there are contradictions in the sequential, or in parallel, the model is expected to resolve that before generating a final answer.

**40:23** · So in that case, it's a little difficult to say because both approaches can suffer from contradictions in the thinking.

**40:33** · But here, what we are seeing is more that these plans are rather than being different approaches to solve the same problem, they're different steps to solve one problem.

**40:48** · So another interesting observation was that-- and perhaps intuitive some that harder problems require more iterative planning and execution.

**41:04** · The other observation-- this was maybe less intuitive was that in the early stages-- so we have a bunch of these parallel planning execution, parallel planning execution.

**41:15** · In the early stages, the more parallelism, or more exploration is observed by the model, and then in the later stages, we converge to maybe to less plans.

**41:35** · Basically, the exploration is more in the early stages, and towards the end, we want to really go dive deep into a single plan and execution.

**41:44** · Yes.

**41:46** · How can you ensure that the independent reasoning tasks are evenly load balanced and do not encounter bottlenecks?

**41:54** · Do independent tasks, for example, have similar expected execution times?

**42:00** · Here, you are saying that how do we make sure?

**42:04** · So when we divide independent tasks, how do we ensure that these are going to be executed in about similar times?

**42:13** · So the question is, how do we ensure that these independent plans that are now run at the same time, they take similar times?

**42:23** · So the thing is we can ensure that.

**42:27** · There are some measures taken to enable that, but we still could have a straggler.

**42:32** · Maybe step 2 versus 4 here, step 4 may take a lot longer than step 2, but at the same time, we are confined to just step 4, not step 4 plus step 2 runtime.

**42:46** · And we have some measures.

**42:47** · For example, if the execution is just too simple, we merge that into the plan and try to create these bigger and bigger chunks that we can do in parallel, but that could be an optimization as well, the optimizing this across the stages.

**43:07** · So I was wondering if there's a group analysis for it \[INAUDIBLE\]?

**43:12** · I'm not sure.

**43:13** · I'm not sure if there's analysis exactly on that.

**43:18** · Question?

**43:19** · Yes.

**43:20** · Could you go back to the slide?

**43:22** · So I saw on the MATH and GPQA, the SPRINT has comparable accuracy and number of tokens as the baseline.

**43:31** · So I'm curious, for those benchmarks, what is the mean width of the tree, and what's the maximum width?

**43:45** · In terms of because the width of the tree determines how much parallelism you can exploit.

**43:52** · So what you're getting at is that the width is task-dependent, basically?

**43:57** · Yeah.

**43:58** · The parallelism that we can exploit, and for some of these, basically if the ratio of the sequential tokens is for one task.

**44:09** · For example, I believe, for MATH is lower than for GPQ domain, then yes, that's an indication of parallelism.

**44:18** · Some tasks could be inherently more parallel than the other.

**44:22** · And I don't know the exact number of the width of the tree here, but that to be able to leverage this approach, parallelism should exist.

**44:31** · But what we observed is that that is the case for many of the reasoning problems like MATH and other reasoning tasks in GPQA and so on.

**44:41** · And some of these are-- again, for example, if you look at this for the MATH data set compared to some of these methods with even lower, but comparable accuracy, we are increasing the bandwidth, or reducing the number of sequence token by something like 40%, which is a long, large number.

**45:12** · But it is true that this is going to be task-dependent.

**45:19** · And maybe getting back to your questions, we have larger savings for problems that need more thinking.

**45:27** · So for example, here we are showing the sequential token reduction by SPRINT over the baseline.

**45:35** · Sorry, over the RFT model.

**45:38** · This is the rejection fine tuning methods, so this is a baseline we are comparing with.

**45:45** · If the number of tokens in generated, like in the thinking process is small, then there is probably less opportunity for parallelism.

**45:57** · So by doing this, oh, let's plan and execute, actually, we can be worse than the baseline.

**46:05** · But this appears in the harder problems and problems that require more thinking and more number of parallel tokens, and that's where this method shines and shows in parallelism.

**46:17** · I'm not sure how many of you have read the recent Sonnet 4.5 system card, but it was very interesting to me that it says, the prompt for the system card encourages the model to use tools as much as possible, and, at least, 100 times.

**46:35** · That's a very large number that the model is encouraged to use the tool.

**46:40** · And this just shows that we are going into this regime that we are solving more and more interesting problems, and we are actually going more and way beyond 8 to 10k, even for the number of tokens that the model deals with for solving a problem.

**47:00** · Yes.

**47:02** · So can you come back to the fine tuning of data set diagram with all the trees?

**47:10** · Fine tuning process.

**47:13** · I think one.

**47:14** · Yeah, there.

**47:15** · Doing inference, does it reduce the entire step 1 to step k the entire thing, but different layers, or does it do a sequential?

**47:25** · No.

**47:25** · During inference, it just likes this.

**47:29** · So the model learns to generate plans that can be executed in parallel at the same time, so it first generates plan 1 and 2, and then once plan 1 is outputted, execution of plan 1 starts.

**47:47** · Once plan 2 is outputted, execution of plan 2 starts, then the result is put back in the context, and then the model is generating two more plans.

**47:58** · So the model still takes this sequential approach to generating plans and execution, but the difference is that if it learns, or is trained to at each point of time, if there are plans that can be executed in parallel, it generates those at the same time.

**48:16** · So here, would be after step 1, it generates step 2 and 4 at the same time, and then you see the results for that and then so on and it continues.

**48:31** · So think about it, each step is a plan and a set of executions in the training.

**48:42** · But this step here is defined as plan 1 and exit 1, and then it be changed the notion of-- Do they also match this?

**48:55** · So let's say, they execute two plans that can be parallelized, and then they collect the context and then add it to the prompt for the next level.

**49:06** · Do they also do that in the training phase as well to match how they are proping it?

**49:13** · This is how the training data will look like.

**49:17** · So plan 1 and 2 are independent, so plan 1 and 2 are put together next to each other, and then we have execution 1 and 2 during training.

**49:26** · So that's how the model sees during training that plan 1 and 2 could be outfitted together, but at inference, the execution is actually also done in parallel.

**49:42** · Let's move on to the last paper because I want to make sure we cover that.

**49:47** · But just before that, opportunity.

**49:50** · So here, the work that supervised fine tuning, but, of course, methods like RL and GRPO can enable potentially much more benefit from this data and much more this generalization property usually works well with RL.

**50:10** · And other notions about tool use, overlapping different tools, or actually realizing the wall clock speed of this other work that can be done here in the implementation of this method.

**50:25** · So now, let's go through another method called SWiRL.

**50:29** · This is also a continuation of multi-step synthetic data generation and helping the model do multi-step better.

**50:41** · And this is a work that is going to be presented next week at COLM in Conference in Language Modeling in Montreal.

**50:48** · So this is another just a preview.

**50:51** · This is another training.

**50:53** · We are using training and basically fine tuning a language model to help it do multi-step reasoning better.

**51:00** · So motivation, again, many real world tasks require multi-step reasoning and tool use.

**51:05** · For example, if you want to answer multi-hop question using a search engine, you want to solve math problems, or use solving a software engineering like doing a project, planning a trip, analyzing data, and so on.

**51:19** · Usually, we go as humans, we use these tools, and reason through them for important tasks more than one, so we need a cohesive number of steps of reasoning and tool use in order to solve a problem.

**51:35** · So the challenges, again, in multi-step reasoning and tool use setting is that then you're doing reasoning and tool use.

**51:45** · Even for one step, it can get complicated, but as we expand on this and generate multiple steps of reasoning and tool use, the errors and the complications can compound over these different steps.

**52:01** · If we want the model to-- and another focus of this paper is enabling tool use, like teaching the model to use the right tools, for example, a calculator, Python executor, and so on.

**52:13** · Using these tools live during the training process can be very challenging because tools can fail, they can be slow, and the training process is already time consuming and challenging, so this can further slow that down.

**52:31** · And if you look back in terms of the fine tuning processes, such as reinforcement learning from human feedback, from AI feedback, or execution feedback, many of these are optimized for single step tasks.

**52:48** · Basically, the model takes a lot of whatever it wants to do, generates a final answer, and the reward is just based on the final answer, whether it's correct or not, and then we back propagate that towards actions.

**53:02** · And here, we want to have more of governance on the process of generating these steps and how we can optimize them.

**53:15** · So this framework called SWiRL, and the design goal for SWiRL is the following.

**53:24** · First of all, at a high level, we want the model to solve complex problem and multi-step reasoning task.

**53:32** · We want the model to know when to call a tool, generate the right queries to invoke a tool, because we need to know how to use a tool, the model needs to know that, carry out these reasoning steps and maintain accuracy across them, and learn how to recover from an error and learn when to stop taking new steps and calling new tools, and say, OK, I'm now ready to generate a final answer, so we want the model to know these steps.

**54:06** · We also want to avoid using tools during the training process, because like I mentioned, this can be slow.

**54:15** · Tools can fail, and can have bugs, so we want to avoid that.

**54:20** · And ideally, we want the model to generalize this, so ideally, we want the model to learn when to adapt to new tools and new reasoning tasks and capabilities.

**54:34** · So to approach this, here is the process.

**54:40** · The first step of this process is that let's start with creating synthetic multi-step data for a model, so given a prompt-- and in order to really annotate these steps, let's have the model take one step at a time and let the model know at each step that it's free to reason, create a chain of thought, call a tool, or propose a final answer.

**55:15** · So having an input prompt at step 1, we tell the model, you have access to these tools, you can generate a reasoning step.

**55:26** · If you're ready to generate the final answer, just say that and create that.

**55:31** · So given this prompt, the model would take the first action, which could be a reasoning step followed by a tool call, and then we show the model the environment response.

**55:49** · So given that, then we show the model again the same prompt, but this time, we have the context from the previous step.

**55:59** · So basically, we say, here is the original prompt, here is the previous action, and here is the result of taking that action from the environment.

**56:08** · You can take a new action and call a tool, or if you're ready to create a final answer, just output the final answer.

**56:19** · So by design, through this adapt to iterative prompting, we are creating this multi-step data set, and the steps can be from 1 to 3 or 5, and so on for different queries.

**56:37** · Then we need a label.

**56:40** · We want to have a notation of how good this step is, and to do so, we ask an LLM-as-a-Judge, given the prior context and the current action, which is a reasoning step, followed by a tool called, give us a reward function, or give us your estimate of how good this trajectory and final action is.

**57:10** · Given that we have for each query and we have a set of steps, and for each step, we have a LLM-as-a-Judge score that is assigned to that step.

**57:22** · And we can do that offline.

**57:24** · We can go through many, many questions in parallel offline and generate these steps and labeled annotations.

**57:33** · Once we have these steps per prompt, we can filter this data in different ways.

**57:39** · For example, we can only keep the data, where the LLM-as-a-Judge decided every single step was a good step.

**57:51** · Every single action was good.

**57:53** · Or we can go based on outcome filter data, and that would be we keep all the trajectories that the final answer was correct, no matter what the label per step was.

**58:04** · And we're going to see how these two differed with each other.

**58:08** · But the whole intuition, motivation behind this part is that, for these reasoning prompts, we have a number of steps, and then for each step, we have a reward created by the model, which we can use or not use during our training, but let's see how these two play out.

**58:32** · Then having this data that we have generated offline, we can start the training process, and the training in this part is done based on reinforcement learning.

**58:44** · So maybe you can pay attention to this figure on the right.

**58:47** · This is a very simple example, but let's go through that.

**58:50** · Who is older, Glenn, I don't know the last name, or Ross Lynch?

**58:55** · So these two people, who is older?

**58:57** · So action 1 is to figure out who is older.

**59:01** · I should first search for age of the first person.

**59:07** · Then we have a reward for this action.

**59:09** · We ask the judge, LLM-as-a-Judge to say given an input prompt and this action, what is the reward for this step?

**59:21** · Then we actually go and show the model the result of this step.

**59:29** · This is already we have in our training data, so we have the environment response, and then we prompt the model to take the next action.

**59:37** · And then the next action is this second question, which is about the age of the second person.

**59:42** · We have a reward based on that.

**59:44** · And at the last stage we say, given the result of the previous searches, we asked the model to generate another action.

**59:55** · In this case, the model seems to be ready to output the final answer, so it outputs the answer in these tags answer and the final answer is there, and we can get a reward based on that.

**1:00:11** · So the point that I want you to pay attention to is how we manage to not have the tool calls during training.

**1:00:18** · So basically, what we are doing here is that we have this trajectory from the prompt and from these pre-collected actions and tool calls.

**1:00:34** · During RL process, we get the reward.

**1:00:38** · We show the prompt and steps and actions onto that action k, in this case, for example, up to action 1 and the environment response, and then we ask the model to take the next step.

**1:00:52** · So this is the part that is done during training.

**1:00:54** · The model takes the next action, but we don't need to execute that action or call the tool.

**1:01:02** · We just collect the reward based on that specific action and use that for RL optimization.

**1:01:11** · All the tool calls are just done during the data annotation process outside of the RL fine tuning part.

**1:01:18** · Because we realize that the LLM just does a good job based on the quality of the action that's proposed, we're good in just evaluating that.

**1:01:29** · We don't need to execute the action and evaluate that.

**1:01:33** · So that's how we separated the two.

**1:01:36** · Do you need to train LLM Judge with this for use?

**1:01:42** · So we did not train an LLM-as-a-Judge for this.

**1:01:46** · We just prompted-- I'll talk about what models we used for each one, so there was no training for that.

**1:01:55** · But if you the judge cannot see the real output from the tool use, how do you \[INAUDIBLE\]?

**1:02:07** · So the question is if the judge cannot see the output of the tool, how can it give a reasonable score?

**1:02:14** · So here's the point here.

**1:02:16** · So we are asking the judge to judge the quality of the query that is generated by the model to call the tool, rather than the output of the tool.

**1:02:28** · Like here, what the judge sees is that the model is asking age of this person.

**1:02:35** · And the model can judge that this is a good question to create for the search engine before seeing the result of the search engine.

**1:02:45** · The model doesn't need to know the age of this person to know this question was good or bad.

**1:02:50** · This is a good question.

**1:02:51** · This is a reasonable question.

**1:02:59** · So basically, what we are doing is providing this process feedback, process reward for this step, and the tool calls are captured in the prior context.

**1:03:09** · So all of these tool call resources, we have collected them in our offline training data set.

**1:03:15** · We are not doing that during the actual RL fine tuning.

**1:03:21** · So to just show you the objective function that is being optimized in this multi-step RL is, let's say we have a number of steps S1 to SK, and then for each followed by an action, which is a reasoning step followed by a tool call.

**1:03:40** · What we are doing here is that we are optimizing the expected reward of a single action, given all the context so far, which is a set of states and actions that we have collected also.

**1:04:00** · So that's how we are optimizing the expected reward of a single action in a multi-step process, given all the prior steps, but, of course, this varies from action 1 all the way to action K.

**1:04:18** · Now, during inference once we RL this model, let's walk through an inference process of how we encourage the model to do this multi-step process.

**1:04:29** · So, for example, here the prompt is help me answer the following questions in just a few words.

**1:04:39** · And then we specify the tool that the model can use, in this case, a calculator.

**1:04:44** · If you think it would help to use a calculator, please generate a mathematical query enclosed by these kind of tags.

**1:04:55** · And then we also tell the model, once you have enough information, you can generate an answer tag and generate the final answer.

**1:05:05** · So through these tags, the model can tell us the tool call, or if it's ready to generate the final answer.

**1:05:13** · So here is the input question.

**1:05:17** · So in step 1, the model is prompted.

**1:05:20** · Here is the input question, the model responses to that question.

**1:05:27** · And in this response is calling it the calculator, and it's calling this is the math that it wants to run.

**1:05:35** · The user provides that output.

**1:05:38** · Basically, that tool is executed with that given input.

**1:05:42** · We give the output to the model, and then the model is prompted again.

**1:05:47** · Again, here is the input.

**1:05:49** · Here is the result from the previous thinking process and tool call, and the model takes the next action, and next action and so far.

**1:06:02** · So we are iteratively prompt the model.

**1:06:04** · Here is what happens so far.

**1:06:05** · Here is the tool you have.

**1:06:06** · If you're ready to generate the final answer, do it.

**1:06:09** · If not, continue using the tool.

**1:06:16** · So the experimental setup for this approach was the following.

**1:06:19** · There is a model Gemma-2-27b was used to create this multi-step synthetic data.

**1:06:28** · The questions were coming from HotPotQA and GSM8k.

**1:06:34** · We had something like 50k sourced from a number of problems and created for different kinds of data that were, like I said, we can process this data that we created based on process filter, outcome filtered both process, and outcome filtered or random.

**1:06:55** · And then we also collected a number of trajectories, I think.

**1:07:00** · So let's take a look at impact of data filtering on the performance of SWiRL.

**1:07:07** · One perhaps in the beginning, this was non-intuitive, but we realized why this is happening is that it seems like when our training data was only processed filtered, meaning we took reasoning steps that were majority like voted yes by LLM as a Judge from the reasoning steps, but we like didn't filter them based on the correctness of final answer.

**1:07:35** · This seems to help the training more than if we rigorously only took trajectories where the outcome was correct, or both process and outcome were correct.

**1:07:51** · And the reason for that is if we only get trajectories, where the model already knows the outcome and is correct, perhaps you're not helping the model solve problems that it couldn't solve during test time, because we are training it to think differently about these problems, so it can solve new problems that it couldn't solve before, but it had gotten the sum processes correctly.

**1:08:19** · But perhaps the most interesting, and this is, again, something that we are seeing in the SPRINT project as well, is the generalization performance of the model.

**1:08:29** · So for example, we had SWiRL on GSM8k.

**1:08:34** · These are MATH problems, and we were teaching the model to use SymPy, a calculator basically, to solve these problems.

**1:08:42** · So that was the training data.

**1:08:44** · And then once we do this multi-step optimization using GSM8k, we then tested on HotPotQA.

**1:08:54** · And this is the accuracy that increase that we get from the base model, so it goes from 65 to 71.

**1:09:03** · And if we were to use exactly HotPotQA, and in this case, the tool for HotPotQA was a search tool, not a calculator, the increase was from 65 to 73.

**1:09:17** · So and vice versa, this was true as well.

**1:09:20** · If we train the model on HotPotQA with a search tool, it could also do well on GSM8k with Python.

**1:09:27** · So it seems like there is something going beyond just like learning to use a specific tool, rather, the model is learning how to think in steps and how to learn how to invoke a tool.

**1:09:43** · And these data sets, the other data sets are separate from any of our training data.

**1:09:51** · Another important observation here was that, again, in this case, the model is being trained on HotPotQA using a search tool for all of these, but we are showing the test results as we are increasing the synthetic data, the training data size.

**1:10:11** · So it seems like as we go from 100 training examples to 10,000 training examples, even at inference, the model is improving on a completely different task, which is MATH problems and GSM8k.

**1:10:25** · So this is, again, it's the most important graph from this paper showing that by creating synthetic data in environments that are perhaps easier to create these data for, and teaching the model how to use these tools and how to do things in multiple steps, we can generalize these behavior to entirely new tools and domains.

**1:10:53** · And perhaps, scaling this up could be a very powerful methodology.

**1:11:05** · And here, we are showing some results to try to interpret why the model is becoming better in through this RL processes.

**1:11:20** · And what we did here is to look into the average process reward per step of the model in answering these questions before and after being fine tuned through this reinforcement learning process.

**1:11:36** · And perhaps this is, again, very intuitive that the process correctness of the model has improved throughout this process for both in-distribution domain, where we train on HotPotQA, and out of distribution when we just tested on GSM8k.

**1:11:52** · So the model thinks more correctly per step, both for on the training data, but out of distribution data.

**1:12:02** · And here are some other results that we also looked into precision, recall, and other metrics across a number of tasks.

**1:12:15** · And here are how this works compared to frontier models.

**1:12:23** · Something that perhaps is worth noting here is that we could do all of this.

**1:12:32** · That all of this process that we did with RL, we could do it with supervised fine tuning as well, and it turns out that this multi-step RL does better by a good amount over supervised fine tuning.

**1:12:47** · And especially for supervised fine tuning, it seems like the model really benefited, like the training data needed to be correct, both process and outcome filtered.

**1:12:59** · Supervised finding on that kind of training data worked better than when we selected only the process filtered data.

**1:13:09** · And it makes sense because in supervised fine tuning, it's an imitation learning.

**1:13:16** · We are showing these are the trajectories, and we want the model to repeat those in a way.

**1:13:21** · And then if they're incorrect, the outcome is incorrect, it might hurt performance, whereas in RL, we are giving the model a new chance to take a new action within the prior steps.

**1:13:34** · And we are giving a reward based on that new action, and that's how it can break out from this.

**1:13:41** · And here are some other results, but because we are out of time, let's just take a look at the summary of this.

**1:13:51** · So again, a important observation was that soil of generalizes across data sets and tools.

**1:13:59** · It transfers to disparate task, and the model learns better from process filtered data, and it can get a lot of gains from more synthetic data, both for in domain and out of domain.

**1:14:14** · And from just understanding why this happens, it turns out that after this fine tuning, the process correctness of the model improves, so if we just go to evaluate that, the model becomes better at this multi-step thinking.

**1:14:33** · Again, this is true for both in-distribution and out of distribution data.

**1:14:38** · And with that, we can conclude this lecture.

**1:14:42** · I hope you learned more about multi-step and reasoning and planning, which is a very active field that is going forward.
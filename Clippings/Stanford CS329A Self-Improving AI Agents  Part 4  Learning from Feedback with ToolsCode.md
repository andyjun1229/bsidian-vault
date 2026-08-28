---
title: "Stanford CS329A Self-Improving AI Agents | Part 4 | Learning from Feedback with Tools/Code"
source: "https://www.youtube.com/watch?v=Lxh9RF5S-K0&list=PLangBM27OtEA&index=4"
author:
  - "[[Stanford Online]]"
published: 2026-08-03
created: 2026-08-26
description: "Want to dive deeper? This curriculum is covered in the following online courses:- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html- XCS329 graduate course:"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=Lxh9RF5S-K0)

Want to dive deeper? This curriculum is covered in the following online courses:  
\- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html  
\- XCS329 graduate course: https://online.stanford.edu/courses/cs329a-self-improving-ai-agents  
  
A similar curriculum is covered in XCS329z https://online.stanford.edu/courses/cs329z-engineering-ai-agents  
  
Follow along with the course schedule and syllabus: https://cs329a.stanford.edu/  
  
Aakanksha Chowdhery  
Adjunct Professor of Computer Science, Stanford University  
  
View the course playlist: https://www.youtube.com/playlist?list=PLangBM27OtEA  
  
Video Summary:  
This lecture recording from Stanford's CS329A, Self-Improving AI Agents, taught by Aakanksha Chowdhery on October 3, 2025, covers three approaches to improving language models through feedback. ReAct interleaves chain-of-thought reasoning with tool-calling actions and is evaluated on HotpotQA, FEVER, and WebShop. RLEF, or Reinforcement Learning from Execution Feedback, trains coding agents using public and private unit test results within a PPO training loop, evaluated on CodeContests. Constitutional AI, developed by Anthropic, uses a written set of principles along with model self-critique and revision to train a preference model through reinforcement learning from AI feedback rather than human feedback. The lecture compares how each method sources its feedback signal, from environment interaction to execution results to AI-generated critique, and reviews related work including WebGPT, Code Monkeys, and SWE-bench.  
  
Speaker Bio:  
Aakanksha Chowdhery  
Adjunct Professor of Computer Science, Stanford University  
  
Dr. Aakanksha Chowdhery is pushing the frontier of agentic LLMs, focusing on recursive self-improvement and long-horizon agents that learn and deploy in the real world. She is one of the few researchers globally who has led frontier model training end-to-end, across both dense and mixture-of-experts (MoE) architectures. At Google, she led the 540B PaLM model, the largest densely trained language model in the world at the time. She subsequently drove pre-training and scaling of Gemini's MoE models across multiple generations, and contributed key components to PaLM-E, Med-PaLM, and the Pathways infrastructure underpinning Google's large-model efforts. She went on to build and lead pretraining teams for open intelligence efforts at Reflection and Meta. Earlier, she held research roles at Microsoft Research and Princeton. At Stanford, where she earned her PhD, she teaches CS329A (Self-Improving AI Agents) and serves as Program Chair for MLSys 2026.

## Transcript

**0:05** · In the first lecture, that be covered is that large language models are really good at solving natural language processing problems, and I think most of you are very familiar with using them in chatbot scenarios.

**0:17** · But to make them useful in real-world tasks, they do need to be able to interact with real-world environments, tools, and code, and learn from what they interact with.

**0:28** · So you already saw some examples of test-time compute and robust verification that Azalea covered in the last two lectures.

**0:35** · Now, we'll build a little bit more on top of that.

**0:38** · So today's lecture, we will focus on three different papers.

**0:42** · The first paper will start with the notion of tool calling, and how can we get the models to go beyond just reasoning to also take into account actions via tool calls?

**0:53** · And the paper that we'll cover here is called ReAct, which actually was one of the first that went around to combine reasoning and acting in language models.

**1:03** · The second paper that we'll look into is RLEF or grounding code LLMs in execution feedback.

**1:09** · What this will focus on is how do you actually do code generation while using execution feedback from being able to run the code or run the tests of the code.

**1:20** · And the third thing that we'll look into is constitutional AI, where we use the model critiquing itself as a feedback loop to improve the model.

**1:29** · So all three of those techniques are ways for the model to improve itself.

**1:34** · But what differs in each of these techniques is, where is the feedback coming from?

**1:38** · It's some form of interaction with either the environment or some form of critique mechanism or grounding using what we know should be the right answer.

**1:48** · So let's start with tool calling as the first abstraction.

**1:56** · So what ReAct really tried to focus on was this notion of when humans want to go and do some action, they think about it first.

**2:05** · For example, if you decide that you want to come take a class, you think about how that might actually help you.

**2:13** · And what this roughly means is that, once you have thought about it, then you will have a reason to act.

**2:20** · And then based on that action, you might observe that you have a new observation about the environment.

**2:25** · So once you come to the class, you might decide you like the class or you don't like the class.

**2:29** · And based on that information, you come up with new reasoning.

**2:33** · Maybe you'll go do the homework, and then that will make you decide something else.

**2:36** · So there is this loop between thinking and action that helps us function as humans.

**2:42** · A similar loop can be very useful in terms of refining what language models generate.

**2:48** · And typically, when you look at language models, they have struggled to combine reasoning and acting by themselves as isolated processes.

**2:57** · In today's models, the reasoning has become innate because thinking has become part of the models.

**3:02** · But if you look at the history of the LLMs in the last couple of years, this was not something that came out of the box.

**3:09** · And one of the challenges of why it was hard for models to combine reasoning and acting is because they typically will hallucinate.

**3:16** · They will have no context of what is actually happening in their environment.

**3:20** · So, for example, if you were to type into a model like Gemini or ChatGPT or Claude, what is the temperature today?

**3:30** · Where is something happening today?

**3:31** · It has no information about the current events, unless it actually goes and does a search call and then fetches that information.

**3:39** · So it has no notion of grounding in the real world.

**3:42** · And as a result of that, it cannot go and take actions, and then actually combine that back into reasoning.

**3:49** · So ReAct was one of the first abstractions that tried to combine it in a way that would be effective.

**3:54** · And what you see today's models do is actually go beyond ReAct to do this in the chain of thought itself.

**4:02** · So let's take a look at what we covered in lecture 1.

**4:05** · So if you look at chain of thought by itself, chain of thought already gives the model some sense of reasoning.

**4:11** · So if you gave it a math problem, the model will show the steps, the intermediate steps, it takes to get to the answer, but these steps may or may not be grounded because they are based on models internal state.

**4:22** · They have no feedback from the external world.

**4:25** · And then there is a second class of LLMs that were developed, for example, WebGPT, which go and interact with, say, web browsers.

**4:31** · And what they're basically learning is how to interact with web browsers, which is a form of a tool.

**4:37** · So they don't necessarily have a reasoning process, but they're basically learning how to interact with web browsers.

**4:43** · So you basically can fine-tune on traces that are interaction traces with web browsers, and then what do humans prefer?

**4:51** · But as a result of those two different things, one is focused more on reasoning and one is focused more on actions.

**4:58** · How do we combine these two paradigms where we can both reason and act in a useful way?

**5:03** · A very simple abstraction that ReAct came up with was just using prompting.

**5:08** · You can get the model to generate verbal reasoning traces.

**5:11** · So first, you say, OK, I want the model to go do this task and ask the model to think, say, step by step about it, and then it comes back with its reasoning trace.

**5:20** · You append that in the prompt, and then you say, OK, what action should be taken based on that?

**5:25** · And then you go take an action.

**5:27** · This really helps the model improve performance where grounding matters.

**5:32** · So HotpotQA, for example, is a question-answering task.

**5:34** · Then FEVER is a fact-checking task.

**5:36** · So these require real-world knowledge.

**5:38** · They require knowledge about what is happening in the world.

**5:41** · And then WebShop, for example, is a task where you're supposed to ask the model to go buy products on the internet.

**5:48** · So it's supposed to do a series of tool calls to actually identify what product to search, and then have sequence of those actions to actually complete the purchase for the user.

**5:58** · So each of these tasks require some notion of grounding in the real world.

**6:02** · And without that grounding, it's not possible for the model to keep making progress.

**6:07** · A second benefit of having the model explicitly do reasoning and action steps is that it will allow the model to give traces that are more interpretable, and interpretable allows humans to really trust the model's responses.

**6:22** · It's almost like getting the model to break down what it's doing step by step.

**6:28** · So what you might be familiar with is that, if you prompt the LLM and you ask it to think step by step, which we were showing in earlier examples, then you will get some form of a reasoning trace where it shows its intermediate steps.

**6:40** · And then, if you ask the model to, say, do a tool, call go search, for example, Google or find the temperature, it will go call an API, and it will get a bunch of observations.

**6:51** · So that would be action only.

**6:54** · Typically, you will have a list of actions if you have a list of tool calls that you are valid.

**7:00** · What ReAct does is it will take a goal and have some form of reasoning, so that will be the left loop.

**7:06** · And then based on those reasoning chains, it will go and act.

**7:09** · That will be the loop in the right.

**7:14** · So what this is setting up is a full agent in itself, where you have some observations about the world and then some set of actions based on what's the context.

**7:23** · And if you were to, for example, take this entire context with observations and the set of actions that have happened in the past, typically, you could go learn a policy, but that would require a full loop, which will be complex and expensive.

**7:36** · But you can actually start doing this in language space, which is what ReAct is doing, where it's basically just generating the thoughts in the language space, and those thoughts are not affecting the environment.

**7:47** · And then based on those thoughts, it's then going and taking an action, just in the prompting space.

**7:51** · So it's a very simple abstraction of how to prompt the models to start thinking about these things and generate actions, which are valid.

**8:01** · One interesting concept I'll mention here is that, when you get the models to generate actions in this particular slide, typically, how do you know that these actions are valid?

**8:11** · So one typical way in which you get these models to generate correct actions is to give them a more-- to frame the problem more as a classification task.

**8:22** · So you say that this is the valid subset of actions, and then use that as a way to say, OK, here is your reasoning.

**8:28** · Here is the state of the world, and here is-- what are the valid set of actions to go take next?

**8:32** · And then based on that, it goes and decides, OK, this is the action to take, and then that generally provides a more grounded response.

**8:39** · And in fact, this was also used in another paper that we worked on in collaboration at Google with robotics folks, where the state of the world and all of that requires very valid actions.

**8:50** · So you can't really operate without having a list of actions.

**8:53** · So that provides one way to really grounded knowledge and what actions to take next.

**8:59** · So in terms of implementing this idea in a very simple way, this was done with-- this is an older model, but with the PaLM model with a frozen LLM.

**9:11** · In few-shot examples, the model was given some actions, some thoughts, and some observations, and then asked to go take the next action.

**9:18** · So for the reasoning traces, it was basically seeing actions and thoughts.

**9:22** · I'll show you an example.

**9:23** · And for the decision tasks, it was basically looking at, what's the state of the world?

**9:28** · What is the thinking?

**9:29** · And then deciding whether to reason and whether to take action next.

**9:33** · So you can either go and reason, or you can decide whether I have to reason or take action next.

**9:38** · So let's look through an example and walk through it carefully.

**9:43** · So aside from the Apple remote, what other device can control the program Apple remote was originally designed to interact with?

**9:53** · So this is basically a question from HotpotQA.

**9:57** · If you basically just do standard prompting, the answer that will come back will not be correct.

**10:02** · Now, you can do Chain of Thought where you basically ask the model to go think step by step.

**10:06** · It's showing you all the intermediate steps here.

**10:08** · However, the answer is still not coming out to be completely correct.

**10:15** · Now, let's see.

**10:16** · If we ask it to take some actions where it can do some grounded knowledge, and it can do some search calls, so it goes and sees that, OK, the thing that I'm really needing more information on is Apple remote.

**10:27** · So it goes and does a action on Apple remote.

**10:30** · It gets some observation.

**10:32** · Then it goes and does another search call on Front Row, which is some text that is there in observation 1 and then continues to follow on.

**10:42** · And then it realizes that, OK, this is a discontinued something.

**10:46** · So as a result, there is not really a good answer that it can give.

**10:51** · Now, how does thinking and action interleaving those traces help?

**10:57** · So here, it thinks first that, OK, I have to search for Apple remote, and then find the program it was originally designed to interact with.

**11:04** · So it first goes and searches Apple remote.

**11:06** · It finds the information that-- it's a remote control introduced very early on, 2005, two decades ago.

**11:13** · And it was originally designed to control the Front Row media center.

**11:17** · Then it thinks, OK, so I need to search Front Row next.

**11:21** · So it goes and searches for this.

**11:23** · It's not able to find it.

**11:25** · So then it comes up with a new terminology called Front Row software.

**11:28** · And then it searches that, and it's able to figure out, OK, it's a discontinued media software center.

**11:33** · And then it thinks about it again, so it's able to give an answer based on that.

**11:39** · So basically, the reasoning process is an abstraction, which allows it to come back with better answer than just taking actions and then coming back with answers in between.

**11:48** · And interleaving the thought and action and the observation aspect is basically allowing the model to behave better.

**11:55** · Now, what is happening in the LLMs today where, for example, if you go in the thinking mode of, say, Qwen or other models, you will see this happening automatically.

**12:05** · So if you actually turn on the thinking mode and say, Qwen models, you will see all of this starting to happen because the models have already been distilled on these traces.

**12:13** · So the thinking fusion stuff that happens in several of the open-source models already captures these things.

**12:19** · So they've already learned how to do, for example, tool calls and so on.

**12:23** · Questions?

**12:27** · Yes.

**12:28** · How does the model know what it knows, what to search, or when to search?

**12:35** · Because clearly, you don't want to search on 1 plus 1.

**12:38** · But how do you determine the search?

**12:40** · How do you determine-- I mean, here, it's searching, and then it's basically coming up with-- here, it's getting a feedback.

**12:47** · It doesn't know what it knows.

**12:49** · This is from interaction.

**12:51** · But you already have been trained on Front Row Wikipedia page.

**12:55** · You shouldn't need to search.

**12:57** · Yes, It doesn't need to search.

**12:58** · Yes.

**12:58** · But does the model know whether it knows this?

**13:01** · So I think there's contradictory set of opinions on whether the model knows what it knows.

**13:07** · There is one set of people that will tell you that models are very confident in knowing what they know.

**13:13** · But I think the other side is that, typically, if you were to ask the model to rate its output of, are you confident about an output?

**13:20** · Typically, the models are overconfident.

**13:23** · They're not well-calibrated.

**13:25** · I mean that's a research problem that is still being solved.

**13:28** · So as someone who's designing a application, what you are looking for is not so much knowing whether the model knows what to know, but getting the model to use the right set of tools so that you have grounded knowledge.

**13:43** · Does that make sense?

**13:44** · Yes.

**13:45** · Yes.

**13:46** · With the ReAct on the right, when you're saying with the left loop, you elicit the reasoning to then append to original knowledge.

**13:55** · Will it produce the reasoning of the one or two or three or four initially, and then it goes and just acts for each one, or does the act influence the next reasoning step?

**14:07** · It's interleaved, so it's thought one, then act one.

**14:11** · So it's happening in an interleaved fashion-- thought one, act one, thought two, act two.

**14:17** · So it's basically each one is informing the next.

**14:20** · It's very much like the human process.

**14:24** · You're thirsty, so you, basically, start walking towards the kitchen.

**14:28** · You get to the kitchen, maybe water is out.

**14:30** · So then you decide the next step based on that.

**14:33** · And so you think that maybe I have to go to the supermarket to go do something.

**14:36** · So it's very sequential in that respect.

**14:40** · You can do parallel sampling and all of those tricks, but then you have to explicitly design that process.

**14:49** · Yes.

**14:49** · There's no guarantees as a search result. \[INAUDIBLE\].

**14:52** · So what do you \[INAUDIBLE\] observe \[INAUDIBLE\] is the search result?

**15:00** · That's a great question.

**15:01** · If there's contradiction between the results, then what do you want the-- I think this is a question that the user has to decide if there's not enough consensus.

**15:15** · So typically, one of the things that we covered in second class was that we can get more confidence by doing, say, majority voting.

**15:24** · So you basically say, OK, or you have some way of validating the answer before you give it to the user.

**15:29** · So for the end application, what you care about is the answer is valid.

**15:33** · So you need more guardrails.

**15:38** · But hallucination with search results can be controlled much better than just depending on the internal state of the model.

**15:47** · Other questions?

**15:49** · Yes.

**15:50** · Maybe this is not answerable, but also \[INAUDIBLE\] from the-- I wonder if you have looked at the KV-cache representation of the thought versus the observation and see if there is any sort of interleaving patterns between them, given that the observations are generally given by the environment.

**16:08** · They are not generated by the LLM itself.

**16:10** · So I wonder if there would be these changes in between.

**16:15** · That might be your research project for this class.

**16:18** · There are open-source LLMs that you can work with.

**16:24** · Yes.

**16:25** · It's just a little termination, like technology \[INAUDIBLE\], but I know this is like the action space of ReAct from where it's the actions plus thought source.

**16:36** · Why do we just think of thoughts internal to the policy model, and maybe the action is just like search or finish?

**16:47** · Why do we say source is also part of action space?

**16:51** · We're not calling it part of action space.

**16:53** · We are calling it a separate thing.

**16:55** · It's like actions are on the right loop, and the reasoning traces are on the left loop.

**17:01** · Are you talking about this one?

**17:06** · So I think because the language models are trained on language, typically, they benefit from having the reasoning tokens in the right abstraction as a way to output the right action.

**17:19** · So that's the main reason to have those tokens.

**17:21** · I mean, if you had intermediate representations, then maybe it doesn't matter.

**17:28** · So let's take a look at some results.

**17:30** · So these two tasks-- HotpotQA is a multi-hop question-answering task over Wikipedia, and then FEVER is more of a fact-checking task.

**17:39** · The action space in these two tasks are very much focused on, say, search over Wikipedia pages or looking up a certain string or finishing that, OK, I finished whatever task I was given.

**17:50** · The action space is actually very simple.

**17:51** · It's basically simulating the human interaction with Wikipedia here.

**17:57** · So the baselines here are simple, where you're basically building a prompt.

**18:01** · The standard prompting that you will see as simple prompting, no thoughts, no actions, no observations.

**18:07** · Chain of thought where you're basically asking the model to think step by step.

**18:11** · Chain of Thought, self-consistency-- SC stands for self-consistency-- where you're basically doing majority voting or self-consistency.

**18:18** · Both of those terminologies are exactly the same thing.

**18:20** · And then Act refers to there is no thinking in between.

**18:23** · You're basically just taking actions.

**18:25** · And there is two variants you will see in the table where you can fall back to Chain of Thought, self-consistency if ReAct fails after a certain steps, and then this.

**18:35** · If the majority answer occurs less than half the time, then it can back off to ReAct.

**18:39** · So you'll see this in the results.

**18:41** · So this is an example of when they prompted this large model.

**18:46** · What they found was that ReAct generally does better than action only.

**18:51** · It did not always outperform Chain of Thought, which was interesting.

**18:55** · It outperformed chain of thought in the case of FEVER.

**18:58** · But in case of HotpotQA, it did not always outperform.

**19:01** · But if you combined this Chain of Thought, self-consistency with either fallback or the other way around, then you do actually outperform the standard techniques.

**19:11** · So what that roughly tells you is that there is value in properly combining the model internal knowledge with the external knowledge, and then using reasoning as an intermediate way for the model to arrive at the right answer.

**19:22** · So basically, that allows the model to reason what is the right and accurate information to retrieve here.

**19:31** · And it's basically showing that it's able to use search as a tool to retrieve the right information.

**19:38** · And then another interesting aspect here is that-- what this is saying is, when it's successful, what is happening?

**19:45** · Did it get the correct reasoning traces?

**19:46** · And when it's failing, what errors are happening?

**19:50** · So one of the things that I want to highlight in this slide without going through too much detail is that, in Chain of Thought, hallucination ends up being a major problem, a major failure mode.

**19:59** · But in ReAct, you basically end up having grounded information, and the model is more trustworthy because it has access to this external knowledge base.

**20:07** · So it allows it to make fewer errors because it can successfully retrieve the knowledge via search.

**20:15** · And then there is some difference between prompting versus fine-tuning.

**20:18** · When you can fine-tune, then ReAct definitely does better.

**20:21** · And then, if you can do outer loop, then it does even better, which we'll cover next week.

**20:27** · So then that was knowledge-intensive tasks.

**20:30** · If you were to look at decision-making tasks-- and this can be, say, online web browser experiments or, say, robotics experiments or gaming environments, where we will look at WebShop as an example-- you require the agent to purchase a product based on user instructions.

**20:46** · For example, you're asking the model to look for a nightstand with drawers, and then you're basically evaluating whether the model gets to success when it's interacting in this environment.

**20:56** · It's a simulated environment.

**20:58** · And then you compare it as a baseline to imitation learning.

**21:00** · That's just fine-tuning.

**21:02** · And then imitation learning plus RL, which is basically just supervised fine-tuning plus RL.

**21:07** · And the results that you see here are impressive in the sense that, even compared to, say, imitation learning or imitation learning plus RL, having the reasoning abstraction with ReAct, you get higher score, and you get higher success rates compared to what's the baseline here.

**21:22** · So the score refers to immediate steps, and the success rate refers to getting to the final-- getting success on the action-- sorry, the task that the user had assigned in this particular case.

**21:35** · So ReAct generally outperforms what was possible with just imitation learning or supervised fine-tuning before.

**21:44** · But it's still far below what human experts can do.

**21:47** · So there's still a lot of headroom compared to, say, human experts, as you can see.

**21:51** · ReAct just gets 66.6 versus human experts get 82.1 in this particular case.

**21:57** · And a lot of challenges happen with respect to success rate, which is lower, because if you get any of the steps, because this is a multistep process, then the errors cascade over time.

**22:10** · So we covered ReAct first.

**22:13** · It's basically a simple method that allows you to combine actions and thoughts.

**22:18** · But one of the challenges with this particular approach is that, if you have very large action spaces, then you need a lot more demonstrations that cannot fit in context.

**22:28** · And then since you require a multiple reasoning steps, your inference costs will be higher.

**22:34** · But overall, it's generally shown to have better performance in question answering, in fact-checking in decision tasks.

**22:40** · And then your hallucinations are lower, and you get better decision traces.

**22:46** · So let's have a few minutes of discussion questions.

**22:49** · So what I will do is I will ask the class to think through these questions and talk to the person next to you to think through these questions, and then we'll come back in two minutes.

**23:03** · Let's start with the last question.

**23:05** · Any takers for the last question?

**23:09** · By show of hands, any takers for the last question to summarize what you guys discussed?

**23:15** · What happens if the environment is noisy, if the feedback that you're getting is misleading?

**23:27** · You can make it up on the go if you haven't discussed this one.

**23:34** · OK.

**23:35** · So if the \[? environment's ?\] feedback noisy or incorrect, you can add another layer of reflection.

**23:41** · So that's the agent to reflect on what the environment gives you and then reason about that \[INAUDIBLE\].

**23:48** · OK.

**23:50** · Yeah.

**23:50** · I was thinking maybe it's important for the agent to have an ability to backtrack whenever something doesn't make sense, or if it's going through a chain of thought that doesn't lead anywhere, just being able to backtrack.

**24:04** · Backtracking becomes important because the noisy feedback might lead it down repetitive loops.

**24:09** · Yeah.

**24:10** · Or you could do external retrieval several times and \[INAUDIBLE\].

**24:15** · OK.

**24:15** · Yeah.

**24:16** · So the better confidence metrics.

**24:18** · So you need some way to build confidence over things.

**24:22** · You could have it perform the same task multiple times and take the highest sample \[INAUDIBLE\].

**24:31** · That makes sense.

**24:32** · Basically, you have a better understanding of how confident the model is on this environment feedback.

**24:39** · OK, good.

**24:41** · Any ideas on the second one?

**24:44** · So ReAct is one way you can think about reasoning and actions.

**24:47** · What other cognitive mechanisms should we take into account if we are building these processes?

**24:54** · Yes.

**24:54** · I mean, humans, their permission is very different depending on the task.

**24:58** · Sometimes we rely on our experiences in the past.

**25:03** · Sometimes we think through things step by step.

**25:06** · So it depends on the task at hand that we do that.

**25:10** · So just relying on ReAct and taking an action doesn't necessarily lead us to the right place.

**25:16** · Sometimes you have to actually think and analyze and do reasoning before we actually do any actions.

**25:23** · So I think what you're roughly saying is that there is other thinking mechanisms that perhaps are worth exploring.

**25:29** · One of them what I would phrase it as task decomposition.

**25:32** · Maybe the task is too complex, so maybe I should decompose it into subtasks before attacking it with these approaches.

**25:40** · Or maybe there is something to be said about having parallel approaches to thinking, which someone had brought up here as well, as to like, is this approach better, or is this approach better?

**25:48** · And then having-- Multiple memory, past experiences.

**25:51** · --have memory, past experiences.

**25:53** · So memory is another aspect.

**25:56** · OK.

**25:57** · Yes.

**25:58** · I think humans also try to fine-tune what is the ideal ratio for reasoning to action.

**26:05** · For some tasks, you might learn over time that it's better to think, give it much more reasoning time before acting it out.

**26:12** · And it might be interesting to see if the paper actually tries to train this on different tasks to see what is the ideal outcome to compute a ratio for each tasks.

**26:28** · That's a great point.

**26:29** · In fact, related to that, you'll find that some of the models today overthink because they have really long thinking traces, and yes.

**26:39** · And even for simple tasks, you'll see them have very long thinking traces.

**26:44** · So there's definitely some interesting set of works there of how to get the models to not think too much.

**26:51** · Let's go there.

**26:52** · Yeah.

**26:53** · Another interesting direction would be, given the different model, the number of parameters and maybe some model is better at being able to do the whole tool calling or chain of reasoning or even delegating tasks.

**27:10** · So being able to do based on what models you're working with, supporting those different tasks.

**27:18** · Almost like building a compound system where you benchmark subtasks on different models and then delegate based on the strengths of the model.

**27:25** · OK.

**27:27** · That might be another project idea.

**27:29** · Cool.

**27:30** · OK.

**27:31** · Let's move to the second paper now.

**27:34** · So this one is called RLEF.

**27:36** · It's based on coding agents.

**27:40** · And what it's basically saying is that, when you're building coding agents, one of the things that you want to do is give some feedback for the reinforcement learning loop.

**27:47** · And oftentimes, what really helps is execution feedback, where we can execute and get that feedback.

**27:53** · So RLEF was one of the first papers that showed that with execution feedback, you can actually get much better performance in coding LLMs.

**28:02** · Why do we care about this problem?

**28:03** · So how many of you use Cloud Code today?

**28:07** · OK.

**28:08** · That's almost majority of the class here.

**28:10** · So I don't think I need to explain that a lot of the engineering and coding tasks seem to have been delegated to these agents.

**28:17** · And the aspect that matters more in building these coding agents to be extremely strong is that we need to be able to understand the user intent.

**28:26** · And based on what the code was generated, we need some feedback from the code generated so that there is a way to iterate on top of that.

**28:37** · So what this paper shows is basically an end-to-end RL fine-tuning framework.

**28:42** · The actions in this particular case are generated code, and the observations that I was showing earlier come from execution feedback.

**28:49** · Execution feedback is test feedback.

**28:51** · You're running some tests, and you're collecting output of whether those tests pass or fail.

**28:55** · And you get binary reward based on whether those tests pass or fail.

**28:59** · And then based on that feedback, you can iteratively refine and fine-tuning time and decide to make the model better based on that.

**29:07** · So PPO can be used for this approach.

**29:11** · The two techniques that this paper covers are two-tier test strategy and then hybrid token-turn level policy.

**29:18** · Both of those are very interesting.

**29:20** · So I'll cover the basic ideas here, but I do encourage you to read this paper very, very carefully.

**29:25** · So the core of their framework is an iterative feedback loop.

**29:28** · They're using both training time and inference-time execution feedback.

**29:32** · So let me explain the training time and the inference-time feedback.

**29:37** · So at the very top in the purple block, what you're seeing is that the model gets a natural language problem description.

**29:43** · For example, someone asked you to, say, write a Hello World program.

**29:47** · Then it generates a code solution, which then evaluates on some public set of tests.

**29:52** · If the code fails, the execution feedback is provided to the LLM for another attempt, and this cycle will continue until either the code will pass or it will reach a limit of the number of turns it's supposed to do this loop for.

**30:06** · And then based on this, whatever set of solutions it has generated for passing solutions, a private set of tests will determine what reward to give, and then that will be used in the PPO training loop with RL.

**30:22** · So what here is happening is there are two fundamental phases.

**30:25** · This is the exploitation phase of RL, where it's basically exploiting the current policy through inference-time feedback loops, like whatever policy model you have got.

**30:34** · And on the right side, you have update of the policy based on the execution results, and this allows continuous improvement for the model to self-improve here.

**30:44** · So let's take a look at how this works.

**30:48** · You're given a simple example where you're creating code to detect, say, palindrome substrings.

**30:53** · So that's what the problem statement on the top is.

**30:57** · In the first turn, it generates a basic solution, but the implementation actually fails in the public tests, and there's execution timeout, which is a very common issue.

**31:08** · After receiving this feedback, the model actually generates a better solution where it does some optimization, and now it does pass the public tests based on that feedback.

**31:20** · So you see that yellow block now submits the solution to the private set of tests.

**31:27** · And based on that, it will go and try to improve the model now that the solution is looking better.

**31:33** · One of the key aspects of their approach was that, during iteration, the public test will provide immediate feedback and will help it do better solution development.

**31:43** · But this is a small subset for faster iteration, and this is basically allowing the model to guide and get better solution, while the private tests are completely hidden during the generation process.

**31:55** · So basically, this separation allows it to not go train on the public test, but only use the private test as the way to get signal.

**32:05** · And this is one way in which the model cannot simply memorize the test outputs, because it's getting the execution feedback.

**32:12** · So this, they found, is a very useful innovation in the self-improvement loop.

**32:17** · A second innovation-- so I will actually not make you go through the details of this RL algorithm.

**32:23** · This is basically PPO.

**32:24** · But the one thing I want to stress is that when you're in a language model space, you're outputting tokens.

**32:29** · So you're outputting one token at a time.

**32:32** · In the policy model, they are generating code tokens token by token, so this gives you finer control over the generation process.

**32:39** · But when they're using the value function, they're computing this at turn level.

**32:42** · So this evaluation or the reward is happening over the entire response, and it's using the last token of the prompt.

**32:49** · So there's a single advantage value for all tokens.

**32:51** · So if you were to match this to where we are in, say, RL algorithms, this is closer to what GSPO would do in terms of giving rewards to the entire sequence as opposed to doing it per token.

**33:09** · Yes.

**33:10** · I didn't understand how do you-- where do you get the public license?

**33:16** · It's a test set.

**33:18** · You have a set of tests that you're keeping as public test, and another set that you're keeping as private test.

**33:25** · Say your question again.

**33:28** · So on the left, you said that's part of difference the user can give all sorts of program descriptions \[INAUDIBLE\].

**33:41** · Then this is for the outer loop.

**33:43** · So, for example, CodeContests, there is a set of tests that are combined with CodeContests.

**33:50** · You have to design the outer loop for the model to get better.

**33:54** · You can keep some subset of tests as public tests on which you will do the inference-time feedback, and then some subset of tests you can keep to train the model.

**34:02** · Oh, I see.

**34:03** · Thank you.

**34:04** · Yes.

**34:05** · What does it mean for the test to fail?

**34:07** · When the test is failing, that's basically saying that the solution that the model generated is not correct.

**34:14** · The model itself evaluates that, the correctness, or who evaluates the correctness of-- The test output is fed to the model.

**34:24** · You have failed, and then that's the execution feedback that's going into the LLM.

**34:29** · You're solving this problem.

**34:30** · This is the output you generated, and this is the feedback you got.

**34:36** · This is shown in the example that I've shown here.

**34:39** · This was the first thing, this code solution.

**34:42** · And then the public test failed, so you're appending all of this.

**34:45** · And then this is the execution feedback, and then you're asking it to generate the second solution.

**34:50** · I was just wondering, what's the evaluation process of a fail or pass?

**34:55** · That's an actual running of a test.

**34:57** · It's a Python test.

**34:58** · It's a simple Python function.

**35:02** · In your homework, you will actually-- not for code, but for math, for any problems that you'll actually try some of this out as not execution feedback, but just identifying the error in the generated solution.

**35:22** · So why does this help or what's the benefit of doing this?

**35:25** · So one of the things that this paper showed was that the y-axis is showing solve rates, and on the x-axis, it's showing the sampling budget.

**35:35** · And this is for two different sets, for validation set and for test set.

**35:39** · And even though the results are a little bit older because they're on Llama 3.1, they clearly showed that after RLEF and training on CodeContests, which is competitive coding problems, you clearly get much better results in terms of solve rate.

**35:55** · Basically, solve rate 10 at k means that you're passing at least one out of-- you have 10 solutions generated, and then you're passing a certain number out of that.

**36:06** · So the solve rate definitely goes up with the RLEF.

**36:09** · And the other thing to note here is that this is log scale on the x-axis.

**36:13** · So this is definitely improving with the execution feedback.

**36:17** · Now, why does it help is the other good question to ask.

**36:20** · So the base models typically don't benefit from access to just faulty solutions and execution feedback.

**36:27** · What is really helping here is the fact that when we are giving-- when we are training on CodeContests, we are showing it in each turn, what's the execution feedback?

**36:38** · And with that, you're basically also generalizing to all the other benchmarks.

**36:43** · So it's the error in the solution, that's what's helping the model start to get better.

**36:51** · And this becomes really clear in this particular example where what they're looking at is number of errors in turn 1, the number of errors in turn 2, the number of errors in turn 3, and then the number of code changes being made and the error type.

**37:06** · And this is for a smaller model, and this is for a larger model.

**37:09** · So what you basically find is that with RLEF, as you go about iteratively in turn 1 and turn 2 and turn 3, you have fewer wrong outputs.

**37:21** · And in subsequent turns, you basically start to repair the output.

**37:27** · If you didn't have this iteration loop, then you basically are not making edits that are correct.

**37:34** · So effectively, you are leveraging both the fact that you have higher diversity in terms of the number of samples that you're making, but also your edits are more targeted because you can look at where you made the error.

**37:44** · And that's one idea that you will use in your homework problem as well.

**37:50** · So with the execution feedback, does it also includes the faults you made, the errors?

**37:59** · Does it include any suggestions for how to fix?

**38:02** · It's just getting a sense of this is the part that gave an error.

**38:09** · But these problems are very simple.

**38:13** · The \[INAUDIBLE\] problems are still, I would say, not more than 100 lines of code, so they have much smaller problems.

**38:25** · Yes.

**38:26** · How is the binary feedback enough to create the-- I have a feeling that maybe these were very easy problems, so that binary feedback was enough.

**38:37** · But for a harder problem, you would probably also need to have the error trace or other metadata to actually know how to debug it more efficiently.

**38:45** · That's quite possible.

**38:47** · I think that might make a very good project as well.

**38:51** · Yeah.

**38:52** · Especially in \[INAUDIBLE\], accuracy at the first time.

**38:57** · I feel like reward is binary reward for the final solution.

**39:02** · It means encouraging the model to just repair and repair \[INAUDIBLE\] all together \[INAUDIBLE\].

**39:10** · That's impossible \[INAUDIBLE\].

**39:15** · What's the question there?

**39:17** · Oh, sorry.

**39:18** · So looking at the reward, is it just binary reward or correct or incorrect?

**39:23** · But the model has a freedom to do \[? that in model. ?\] How does this RL method encourage the model to get it correct, get the problem correct, in the first time?

**39:34** · So I think it really depends on the error it made.

**39:37** · And I agree with you that for more complex problems, as was brought up, it is possible that it will take multiple turns.

**39:43** · But if it was a simple enough problem, then-- I mean, if you remember, there's inference-time feedback here also.

**39:49** · And you're appending what is the error that it saw, and you're allowing the public test to pass before you send it to PPO.

**39:58** · So to some extent, it will have had a few chances to go correct itself.

**40:03** · You can always increase the number of turns to finish the problem, like any reward, you think that-- Yeah, you can.

**40:10** · You can try all of those things.

**40:12** · I think these are-- I mean, this is one abstraction of that problem that I'm showing you.

**40:17** · And overall, I think what we want to learn out of here is that the self-improvement loop works.

**40:23** · That's the first thing that we're learning, and it can work in simple enough problems with binary reward.

**40:28** · And then potentially, I think, the question is, between process reward models versus outcome reward models, which works better?

**40:34** · I mean, what you're saying is that, do we need to give feedback at every single step?

**40:38** · And it's possible that that is what matters.

**40:40** · Azalea covered it in last class, the outcome versus process reward model.

**40:44** · So I think that debate is not completely solved in terms of-- in each domain and each benchmark, you might have to make different set of choices to help climate.

**40:54** · Yes.

**40:56** · I might have missed this, but why does it encourage generalization?

**41:01** · Because I think-- \[? isn't ?\] context is more difficult than human level and \[INAUDIBLE\].

**41:06** · And that might be why it generalizes better.

**41:10** · And another is that, what about supervised fine-tuning, would it be able to beat \[INAUDIBLE\]?

**41:19** · For example, \[INAUDIBLE\].

**41:20** · Does supervised fine-tuning model or what always matters?

**41:23** · Supervised fine-tuning on reasoning traces might actually still get you some of the gains, as you probably have papers out there saying that.

**41:32** · But I mean, this is still a question up for debate.

**41:37** · But I think with RL, you are able to solve slightly newer problems.

**41:41** · So there is a little bit more generalization that's seen.

**41:43** · But with supervised fine-tuning, anything that's within domain will definitely start to see value.

**41:48** · It's still the same loss function.

**41:52** · Do this have an ablation of the two-tiered \[? task strategy? ?\] Because one way is you can just have all the tests in public and then run this loop.

**42:05** · And then at the end, you do show.

**42:07** · I see.

**42:08** · So why did they do that?

**42:09** · What do you do with the \[INAUDIBLE\]?

**42:11** · On the final result after the \[INAUDIBLE\].

**42:17** · I see.

**42:18** · I didn't see that ablation.

**42:19** · I think there must be, well, some amount of just like they wanted to use more fine-grained feedback than just the feedback of the public test so that there is no leakage between the two sides.

**42:29** · Where would you care about leakage?

**42:31** · Why would you not care about the leakage?

**42:33** · I mean, they split the test into public, private themselves.

**42:36** · It's all test.

**42:38** · It's not in the training part of the model.

**42:41** · So why do you have to split it into two tiers \[INAUDIBLE\]?

**42:44** · I mean, in the outer loop, if you're training on the thing that you're basically going to use as the feedback, then that aspect matters.

**42:54** · We can take this one offline.

**42:55** · OK, sure.

**42:56** · I think there's a little bit of terminology gap around.

**42:58** · I see.

**43:02** · Yes.

**43:03** · In the ablation study, I was curious why RLEF produces fewer wrong outputs, but more timeout errors.

**43:12** · Oh, because it's probably-- so it's pure wrong outputs because it's able to fix itself.

**43:18** · But then if it ran out of time in \[INAUDIBLE\], basically, the tests ran out of time because the solution was still not correct.

**43:30** · A lot of this is very domain-specific, also.

**43:37** · OK.

**43:38** · I'm actually going to skip this slide.

**43:41** · But I think the main thing that I want you folks to take away is that there is a way to incorporate execution feedback to improve code generation as a domain.

**43:51** · And competitive programming tasks is one place where it has shown promise, and it does generalize to other benchmarks in the code generation realm.

**44:02** · So let's take a look at, say, question 2 and discuss that for one minute among your peers, and then we'll come back together as a class.

**44:15** · Any takers for this problem?

**44:18** · The code base doesn't fit the context window.

**44:23** · So one thing I know is that some tools, what they'll do is they'll do something similar to the previous paper we're discussing, and they'll think about what information they need.

**44:32** · They'll have access to some search tools, and then they will continue iterating on that until at some point, they decide they have enough information.

**44:39** · And then they move on to something like what we are discussing.

**44:44** · That definitely makes sense.

**44:46** · Any other takers?

**44:53** · Yes.

**44:54** · I think he would make this the code of each element \[INAUDIBLE\] for summary so that \[INAUDIBLE\] be something \[INAUDIBLE\], and then together, they can fit in the comments window.

**45:10** · Any other ideas?

**45:12** · Yes.

**45:13** · I don't know if this applies here, but in a regular setting, I feel like you can build a graph-regularized version of your code base and then do a similarity based on what you can find them, and again, do another iteration on that, just simple \[INAUDIBLE\].

**45:30** · And then you can have in the loop what you said about verifying and see if you have enough information.

**45:37** · And then, if not, you can do that, because in that case, you can use the summarization.

**45:42** · You can use the things that you're extracting and then come up with the answer.

**45:49** · So this is actually the kind of thing that actually runs in Cloud Code.

**45:53** · It has to go search for what is relevant and then actually apply the code, and it's there.

**45:58** · And one of the benchmarks that targets this is like SWE-bench.

**46:02** · So all the ideas that you folks have proposed in the realm of searching for something, having some summary, doing some representation, all of those are perhaps the first step to solving that problem before you now do the test, what code patch to apply, and then whether it has passed or not.

**46:21** · So Code Monks paper from Azalea's lab also targets very similar ideas here.

**46:30** · Let's move to the last topic.

**46:32** · The last topic is constitutional AI, where we'll have the model learn from AI feedback.

**46:37** · And the thing that we are improving about the model that is harmlessness, or its ability to generate harmless outputs.

**46:46** · So we want it to be helpful, but we also want it to be harmless.

**46:50** · So what happened with LLMs when they are base models is that you can give them feedback in a lot of ways.

**46:57** · A typical way to give feedback when you are trying to build a chatbot would be that you look at the outputs, and you ask humans to rank them in, is the model output correct?

**47:06** · So you show it two different outputs.

**47:08** · You ask it whether it's correct, whether it's useful, and whether it's specific enough.

**47:12** · And then based on those human preferences, you can build a reward model, and then you can use that to hillclimb.

**47:18** · So here is a Python fine-tuning with RLHF versus just Python fine tuning.

**47:24** · And as you increase the model size, you clearly see better responses with RLHF.

**47:29** · So basically, that's this whole notion of you can use these preference responses from humans as human feedback to hillclimb on the model.

**47:40** · Now, that doesn't scale very well, because if you have to collect tens of thousands of human labels, that's extremely time consuming and tedious.

**47:49** · Imagine that you generate all these model outputs, then you have to ask humans to rate them.

**47:53** · So one of the very interesting principles, given that the models can reason, was to use this notion of constitutional that Anthropic came up with, which was very much based on human-written principles.

**48:04** · So they basically used constitutional AI or human-written principles called the Constitution, and then used them to improve the model by describing what is the desired behavior.

**48:14** · So humans don't need to be in the loop, except to write that Constitution.

**48:17** · And the reason this notion of rules works is because the models get better at instruction following.

**48:22** · So if you ask the model to format the response in a certain way, the model is able to follow that instruction.

**48:28** · Or if you ask the model that, does this response have this particular behavior, then the model is able to actually answer that in truthful ways.

**48:37** · That's what the constitutional AI aspect will be able to exploit.

**48:42** · So what constitutional AI did was it came up with a set of 16 principles, which they call Constitution, and those will define the model behavior, and they use that.

**48:52** · So these are going to be the set of prompts which will elicit whether it's following the Constitution or not, and then use that to critique the model itself.

**49:00** · I'll show you an example.

**49:01** · And then ask you to revise its response.

**49:04** · So you're basically saying whether-- we're basically using some red-teaming prompts.

**49:09** · You're looking at the model output.

**49:10** · You're critiquing it.

**49:11** · You're getting a revision, and then you're using that to fine-tune the model.

**49:15** · And so that's the supervised fine-tuning stage for constitutional AI.

**49:20** · And then this is the RL stage where you're basically doing the same set of responses.

**49:25** · And then using AI feedback to train a preference model, and then using that to train the final model.

**49:31** · I'll show that in detail in just a second.

**49:34** · So before we go there, let's take a look at what might be an example Constitution.

**49:40** · I will not read this word by word, but I'll show you the basic examples.

**49:43** · So the critique request in this particular box diagram that I showed you is that there is a red-teaming prompt.

**49:50** · The model has an output.

**49:52** · And then the critique request is basically asking if the model output has something harmful or unethical and so on.

**49:59** · And the revision request is basically asking you to remove any of those responses.

**50:04** · A second critique request might be that, does it have any gender bias?

**50:08** · And the argument about why that might be having a gender bias.

**50:12** · And then the revision request is, can you remove any trace of that?

**50:16** · And the third one is more like, is it inappropriate for young children?

**50:20** · And then what would it take for it to be appropriate?

**50:24** · And then the revision request is rewrite it.

**50:26** · So if you look at each of these, it requires the model to be able to identify these behaviors.

**50:31** · And then the second thing it requires is to be able to follow the instruction of now rewrite it with this particular style or way, or removing this content.

**50:43** · And then the way this loop works is that humans come in and set right a set of principles that will be used for the self-improvement loop.

**50:52** · In the supervised learning stage, you're basically fine-tuning the model on this data generated by the self-critique and revision stage.

**50:59** · So the critique request, as I showed you, might be something harmful, something unethical, and the revision might be, OK, remove anything that's harmful and unethical.

**51:10** · And just with supervised learning with a number of turns, you are able to-- just with the number of revisions, the harmlessness improves and the helpfulness will decline if you just keep increasing in supervised fine-tuning.

**51:25** · But overall, the helpfulness plus harmlessness will improve monotonically, because if you're trying to get the model to a certain set of fixed principles, then it does become less helpful is what they're saying.

**51:38** · But overall, it's more helpful and more harmless together is their claim.

**51:44** · And then in terms of the reinforcement learning stage, first, they train a preference model based on the responses in step 1 and the Constitution, and then they fine-tune the LLM to maximize over this preference model.

**51:56** · So they're basically getting the model to respond in a way that's most thoughtful, respectful, and cordial.

**52:03** · So this is basically the loop.

**52:05** · So there's a preference model that's being trained separately with this Constitution, and then that's what is being used to fine-tune the LLM to get better.

**52:13** · So instead of the RLHF loop where you had a lot of human feedback, now you're using this preference model, which is trained with the Constitution.

**52:21** · Yes.

**52:22** · So all constitutions, maybe there may be some amendments.

**52:26** · If so, how do you make sure that you're cost efficiently updating the constitutions for this model without having to train all over again?

**52:35** · And if so, how do you make sure that the previous rules are removed completely?

**52:41** · So there's two answers to your question.

**52:43** · So one answer is that \[? AI ?\] is generally done as the last stage of model.

**52:50** · And typically, once you have a pretrained base model, post-training has typically been a much smaller percentage of compute, so maybe 5%, and that happens fairly frequently for models to get updated.

**53:04** · So in that sense, if you do think that the Constitution should be updated, that happens at a certain frequency.

**53:11** · Overall, I think the question you're asking is this notion of continual learning, and how do we get the models to adhere to certain behavior.

**53:17** · I think that's an open research problem at this point in time-- how do we get the models to forget certain set of knowledge or to adhere to a new set of knowledge or to follow a new set of rules?

**53:26** · So that's definitely something.

**53:28** · There are interesting answers to that problem where you can do some canceling of getting it to forget a certain set of knowledge by looking at, say, interpretability methods and so on of like, can you cancel that knowledge?

**53:39** · But then it's not proven that you can get the models to forget something.

**53:49** · So in terms of how this scales, so this is the number of training sequences they're using.

**53:54** · And on the x-axis, they're showing the score of helpfulness Elo.

**53:58** · Elo means that humans prefer it in terms of helpfulness.

**54:02** · And then, similarly, on the right side, they're showing harmlessness Elo where the humans prefer it in terms of it being more harmless.

**54:10** · So now that we have replaced human preferences with AI feedback, we are comparing it to, say, just using helpfulness-based RLHF or helpful-plus-harmlessness-based RLHF, which is all human feedback-based, and then just using constitutional AI and constitutional AI with Chain of Thought.

**54:28** · And what they roughly show is that just getting the model to evaluate its responses based on these principles, you still get the model to be equally helpful, maybe a little bit less helpful, but it's much less harmless as a result. So the harmlessness scores are much higher, and that was something that the Claude models were extremely strong at.

**54:51** · And now that's a set of techniques that are used across the models.

**54:55** · Yes.

**54:56** · The Chain of Thought has lower helpfulness Elo.

**55:00** · Say that again.

**55:01** · The Chain of Thought has lower helpfulness Elo.

**55:06** · Yes.

**55:07** · Results \[INAUDIBLE\].

**55:11** · So it means that Chain of Thought actually worse, the performance.

**55:15** · Possibly.

**55:16** · That's a good point.

**55:18** · Is there a measure?

**55:20** · And interestingly is that, on the right, \[INAUDIBLE\].

**55:23** · So I think the correlation is less with Chain of Thought and more with the fact that, as I showed you in the last slide, this one, anytime harmlessness is going up, there is some amount of inverse relationship between these two.

**55:37** · So it's almost like-- in this particular case, if it was more harmless, then it does hurt the helpfulness.

**55:46** · But overall, you have to find the right balance between these two.

**55:50** · Thank you.

**55:51** · Yes.

**55:52** · Let me go back to step 1 of the Constitution AI to the supervised learning part.

**55:57** · So it said in the slides that we want to fine-tune on the data generated by self-critiquing relations.

**56:03** · So I want to understand whether this just simply means that we want to just reinforce the log likelihoods over literally the generations, the rollouts of the L, of the original policy of L.

**56:17** · So basically, we just ask it to critique itself, and then we just fine-tune this sampled rollouts so that they're more likely.

**56:24** · That's what this stage is basically \[INAUDIBLE\]?

**56:29** · It's a stage that's used in a lot of other things that you will see.

**56:35** · But what this is basically is doing a set of-- these are traces that it's generated.

**56:40** · It's based on reasoning.

**56:42** · You want it to follow a certain set of principles, and then it critiqued itself.

**56:46** · It revised itself, and it got fine-tuned on this set of traces.

**56:49** · I mean, if you were training it for thinking, for example, these would be the reasoning traces.

**56:56** · So I think being trained on-- it's being fine-tuned on those reasoning traces, But I guess it's interesting that there's not really an explicit feedback-- There is no feedback.

**57:06** · --because it's just asked to do this thing, and then we just fine-tune it over what it has tried to do.

**57:12** · But as long as the fine-tuning is not very large scale-- it's much smaller than what the base model was initially trained on-- it will not lose its initial capabilities, but the distribution of what it will output, will start to get biased towards this set of responses.

**57:28** · So I'm pretty sure the foundation \[INAUDIBLE\].

**57:34** · The AI feedback stuff?

**57:36** · Yes.

**57:36** · How do we evaluate whether or not they provide accurate feedback?

**57:40** · That's a good question.

**57:41** · So I think for the preference model, when you do train this preference model, you want to have some sort of test or validation set to make sure that the preference model will do a great job.

**57:52** · So you do want to have some human.

**57:54** · But typically, what you'll do is you will do a lot of AI feedback.

**57:57** · But for the preference model, you'll also get it to give some scores on set of things and then match it with humans.

**58:03** · So you do want to do some sort of consistency with human for preference model.

**58:08** · \[INAUDIBLE\] It's not \[? quality. ?\] It's not scaled to 10,000 or that level.

**58:15** · You're basically able to do based on such compositional principles.

**58:26** · So overall, in terms of results, what this roughly means is that, if you were to plot the harmlessness Elo on y-axis and the helpfulness Elo on x-axis, the pretrained base model is basically the raw base model.

**58:39** · So it will have a certain set of scores, which are not very high.

**58:44** · But with standard RLHF, you will-- if you were doing that with just helpful only, you will start to push that frontier towards getting higher scores on helpfulness.

**58:53** · And then, if you start to make it less harmless, then that's what the orange curve shows you.

**58:58** · But then, if you do Constitutional supervised learning, then you're still worse than doing RLHF.

**59:02** · But when you do Constitutional RL with Chain of Thought, that's where you get the frontier in terms of the best Pareto frontier in terms of tradeoff between harmlessness and helpfulness.

**59:12** · And that's one of the key ideas of this paper as to you can strike the right Pareto frontier between helpfulness and harmlessness in this particular case.

**59:21** · If you were to generalize these set of ideas across-- I mean, generally anything you want to do in instruction following where you want the model to follow a subset of instructions but they might be conflicting-- then this style of principles applies.

**59:38** · And some follow-on work that went and built on top of that includes the fact that there was another work that tried to compare RLAIF with RLHF.

**59:48** · There was self-refine, where it talked about iterative refinements with self-feedback.

**59:52** · One comment that's worth noting here is that oftentimes getting the model to critique itself can be harder, so having a consensus of other models to critique the model sometimes works better because the models might be overconfident and not knowing what they know.

**1:00:09** · And then there was another paper that tried to teach models to self-correct via reinforcement learning.

**1:00:14** · So this is an active area of research, just trying to get the models to be better at self-correction just beyond just the helpfulness and harmlessness paradigm.

**1:00:23** · So that might be another set of project ideas that you might want to explore.

**1:00:28** · So let's recap and then we'll close out the class.

**1:00:33** · So in terms of the ReAct approach, what we first looked at was this notion of, when we talk to LLMs, we can get them to give model outputs and what we wanted these model outputs to be preferable by humans, which has been a focus.

**1:00:48** · But what ReAct starts to look at is this notion of, can we get the models to act in real world?

**1:00:54** · And based on that feedback and combining that with reasoning, we can get them to be grounded so they can give better answers to questions, can check facts better.

**1:01:03** · Or if we put these LLMs as decision makers in, say, gaming environments or in other environments related to, say, web browser agents, and so on, then they can make useful decisions.

**1:01:16** · And one interesting aspect of doing it in ReAct style, in language space, ends up being that the decision traces are extremely interpretable.

**1:01:24** · There are several works on top of that try to combine this reasoning and acting in different ways and trying to get the models to do better tool calling to the point where this tool calling is innate in several models that are out of the box today.

**1:01:39** · But this is the building block of how to get the language models to combine reasoning and acting.

**1:01:44** · A second aspect that we covered today was this notion of RLEF.

**1:01:48** · So in coding agents, getting the models to act in the correct way requires some form of execution feedback, and you want to iteratively incorporate that feedback so that you can generate the right code solutions.

**1:02:03** · For code, one of the best ways to get execution feedback ends up being tests, unit tests.

**1:02:08** · So that's one way the models have been used to self-improve, and this also reduces the amount of budget you need to get the models to get better and get state-of-the-art performance in, say, CodeContests, and other competitive programming tasks.

**1:02:24** · So that's one aspect of just getting execution feedback in the coding domain.

**1:02:30** · And then finally, what we covered was this notion of constitutional AI where we are getting the model to follow a set of constitutions, which is a set of principles written by humans, to generate feedback for self-improvement.

**1:02:41** · In general, you can also generalize it to anything where you can get the model to follow a set of rules.

**1:02:46** · And then based on whether it's following the rules well or not, you can get a self-improvement loop going.

**1:02:51** · So hopefully, with these set of papers, you got a sense of how we can build a feedback loop on top of the models.

**1:02:59** · And when the feedback loop has enough signal, then you have a way to improve the model beyond just what is the data it was trained on.

**1:03:09** · And these were several examples of where this has been shown to work well.

**1:03:13** · Sorry, this slide was not meant to be there.

**1:03:16** · So that would be the end of the lecture, but let's take any questions.

**1:03:30** · OK.

**1:03:30** · This is a really naive question, but are there-- so because a lot of human cognitive thinking is very paralleled in how we're designing elements, is there actual, very systemic research to combine cognitive behavioral science with elements?

**1:03:49** · Or how do we think of new procedures to innovate elements like this?

**1:03:56** · That's a great question.

**1:03:59** · I think where we are right now, that's what we are-- we're using parallels from how humans solve problems because we are in this space of reasoning LLMs.

**1:04:10** · We're in the era.

**1:04:11** · But I think at the end of the day, we're still trying to solve the problem of what would get the models to hillclimb without explicitly saying in words what's the reasoning space.

**1:04:23** · So I think the closed-source LLMs have done better than just saying that this is their reasoning space in words.

**1:04:35** · So effectively, what I'm trying to say here is that you can do a lot of techniques where you can be like, I need to break down the task step by step, which is something that Azalea presented in the first lecture.

**1:04:47** · I need to decompose the task.

**1:04:49** · I need to analyze the task, and send it in parallel loops.

**1:04:52** · And that's how humans solve problems.

**1:04:56** · But at the end of the day, you also want to answer the question of, can that whole process of search in the reasoning space be automated, and is there a well-defined process to do that search?

**1:05:09** · And if the search space is well-defined, then you can automate it.

**1:05:14** · The challenge of why we're doing it, not in an automated way, but in this language spaces, because a lot of tasks that we're giving to these models is not in a well-defined search space.

**1:05:25** · A good example of that would be that, if you were basically in gaming space, where the action space is well-limited and the search space is well-limited, then you can define models to go figure out what the search space is and how to explore that search space.

**1:05:39** · But if we are talking about experience and going and experiencing actual environments, whether that's search tools or everything else, you have to collect observations there and then use that.

**1:05:51** · So that's why you're seeing this.

**1:05:57** · So far, we've been talking about improving LLMs through different techniques.

**1:06:01** · I wonder how those techniques are transferable to improving agents.

**1:06:06** · You will see that in some of the subsequent lectures.

**1:06:09** · But I mean, all of this-- what's your definition of agents versus LLMs?

**1:06:14** · Oh, is basically some LLM that are \[INAUDIBLE\] and memories and sketches that can carry all of us.

**1:06:24** · So I think this is starting to represent what I would call an agent, but not with-- doesn't have sessions, doesn't have memory, because one of the fundamental building blocks of agents is, how do we get the LLMs to respond in a certain way?

**1:06:37** · So this ends up being very useful to understand.

**1:06:43** · So for frameworks, like ReAct, my understanding is that they have some intuition of what kind of \[INAUDIBLE\] thing calls a reasonable help the model.

**1:06:53** · But is there a relationship that only \[INAUDIBLE\] a certain domains, and then does it help versus \[INAUDIBLE\] the other \[INAUDIBLE\]?

**1:07:01** · So now that we have the more RL-based post-training methods, will this handcrafted framework become obsolete?

**1:07:12** · Yes and no.

**1:07:14** · The reason the answer is yes is because, if you can define the search space of what to go explore, then yes.

**1:07:22** · No, because defining the search space for all tasks of what to go explore is not well-defined.

**1:07:29** · If you wanted to do the task of an accountant, if you wanted to build a finance agent, if you want to build a legal agent, what is the set of steps they follow?

**1:07:39** · That's very domain-specific.

**1:07:42** · But it's just generating tokens.

**1:07:44** · \[INAUDIBLE\] is also just tokens.

**1:07:47** · So you're just generating rewards using the reward to supervise them.

**1:07:51** · So I think in an abstraction, I can answer it as yes.

**1:07:55** · But the specifics still matter.

**1:07:57** · So the reason ReAct as an approach matters is because they are basically saying, OK, I can reason that I can take action, then I can go reason, I can take action.

**1:08:05** · So it's basically defining the sequence and the workflow.

**1:08:07** · If you remember from the first lecture when we defined the agent, we said it's basically some abstraction of how I would define that workflow.

**1:08:15** · So how I would generalize the whole ReAct approach to an agent is I would say, OK, this is the workflow that I need to follow to accomplish the task that the user has given.

**1:08:24** · But the workflow to accomplish the task is still very domain-specific, so that's why it's very hard to generalize across domains for everything.

**1:08:34** · Yes.

**1:08:35** · Well, I have a question about the formalism on slide number 12, the methodology setup page.

**1:08:41** · One question I have-- is that there, the way that you define C subscript t, the context, is the context just simply being treated as a state?

**1:08:52** · Yes.

**1:08:53** · OK.

**1:08:54** · I mean, the reason it's called context is that-- I mean, RL state versus prompting is literally what's in the context.

**1:09:01** · No, I totally agree with that.

**1:09:03** · And then the other thing is with ReAct, because ReAct has this thought, and then there's this action.

**1:09:08** · But it seems like in the formalism in page 12, the action, I suppose that action would include, presumably, both the thought and action because since the action from that thought would just be extracted from the output of the RL.

**1:09:25** · So in that particular case, it's being given the choice, so it's basically either outputting a reasoning trace, or it's outputting an action, and it's making a decision whether to output one of those two.

**1:09:39** · So it's-- Oh, I see.

**1:09:41** · So the action can be just like a standalone reasoning trace.

**1:09:45** · And then it stops, and then it does another action.

**1:09:51** · Yes.

**1:09:53** · This might be a naive question, but I was just wondering what this harmlessness have certain features of certain methods structures.

**1:10:01** · So we have \[INAUDIBLE\] obvious considerations instead of just trying to saw in the feedback to try to fine-tune the model to somehow improve the harmlessness.

**1:10:12** · For example, what can we do \[INAUDIBLE\] instead is \[INAUDIBLE\] can use \[INAUDIBLE\] to generate certain methods to restrict \[INAUDIBLE\].

**1:10:25** · Yes.

**1:10:26** · I think that is done to some extent.

**1:10:30** · At the same time, these models are trained on the internet, so no amount of restriction is really going to get all of that out.

**1:10:41** · So it's a game of when you are training on a lot of data, that is the tradeoff.

**1:10:52** · The data is definitely filtering off data that happens.

**1:10:58** · If there are no further questions, we'll call it a close of the class.

**1:11:06** · Thanks, everyone.
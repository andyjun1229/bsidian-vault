---
title: "Stanford CS329A Self-Improving AI Agents | Part 7 | Self-Improvement and Deep Research Agents"
source: "https://www.youtube.com/watch?v=Uni9dqyuuDM&list=PLangBM27OtEA&index=7"
author:
  - "[[Stanford Online]]"
published: 2026-08-03
created: 2026-08-26
description: "Want to dive deeper? This curriculum is covered in the following online courses:- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html- XCS329 graduate course:"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=Uni9dqyuuDM)

Want to dive deeper? This curriculum is covered in the following online courses:  
\- Agentic AI professional education program: https://learn.stanford.edu/agentic-ai-2026.html  
\- XCS329 graduate course: https://online.stanford.edu/courses/cs329a-self-improving-ai-agents  
  
A similar curriculum is covered in XCS329z https://online.stanford.edu/courses/cs329z-engineering-ai-agents  
  
A similar curriculum is covered in XCS329z https://online.stanford.edu/courses/cs329z-engineering-ai-agents  
  
Follow along with the course schedule and syllabus: https://cs329a.stanford.edu/  
  
View the course playlist: https://www.youtube.com/playlist?list=PLangBM27OtEA  
  
Video summary:  
This lecture video from Stanford's CS329A, Self-Improving AI Agents, taught by Aakanksha Chowdhery on October 17, 2025, examines self-improvement through search. AlphaCode pretrains a masked language model on GitHub and CodeContests data and generates large numbers of samples before clustering and selecting a final answer, while AlphaCode2 fine-tunes Gemini Pro with a learned scoring model, reaching an 85th percentile ranking on competitive programming contests. The lecture explains how solve rate scales with sample budget and where selection and clustering become bottlenecks even after large-scale sample generation. It then introduces Search-O1, a method that triggers search queries when a reasoning model expresses uncertainty and reasons over retrieved documents, which outperforms standard and agentic retrieval-augmented generation on GPQA and multi-hop question-answering benchmarks including HotpotQA and Bamboogle. The session closes by comparing Search-O1's prompting-based approach to Search-R1's reinforcement-learning-based approach for teaching models when to search.  
  
Speaker Bio:  
Aakanksha Chowdhery  
Adjunct Professor of Computer Science, Stanford University  
  
Dr. Aakanksha Chowdhery is pushing the frontier of agentic LLMs, focusing on recursive self-improvement and long-horizon agents that learn and deploy in the real world. She is one of the few researchers globally who has led frontier model training end-to-end, across both dense and mixture-of-experts (MoE) architectures. At Google, she led the 540B PaLM model, the largest densely trained language model in the world at the time. She subsequently drove pre-training and scaling of Gemini's MoE models across multiple generations, and contributed key components to PaLM-E, Med-PaLM, and the Pathways infrastructure underpinning Google's large-model efforts. She went on to build and lead pretraining teams for open intelligence efforts at Reflection and Meta. Earlier, she held research roles at Microsoft Research and Princeton. At Stanford, where she earned her PhD, she teaches CS329A (Self-Improving AI Agents) and serves as Program Chair for MLSys 2026.

## Transcript

**0:05** · So today's focus will be very much on improving the models using search.

**0:11** · And there can be two kinds of search that we will see.

**0:14** · One in code models, where we are sampling a lot and then we are searching based on that, and then deep research style search, which you will see in homework three.

**0:24** · So a lot of what we will cover in AlphaCode and AlphaCode 2, those search patterns you will use also in homework.

**0:32** · Your homework two is focused on human eval, so this will give you an overview of what to expect in simpler problems and then even more complex problems.

**0:44** · And then the agent search, this will be closer to what we will give you in homework three.

**0:52** · The broad thing that I want to say with these models is that we know that the solutions lie in the search space of the models, but how do you curate the answer out of the search space of what the model outputs is roughly what we are covering today.

**1:11** · So let's start with AlphaCode.

**1:15** · So the problem we want to solve here is a more complex version of the simple coding agent problem.

**1:22** · So if you use a coding agent, what you often get is some form of an autocomplete, where you have a line, and then the coding agent will complete the line for you.

**1:33** · So this is closer to a competitive programming problem, where given a competitive programming problem, you're given a problem description and then you're given some input and outputs, so you have some a contract in that programming problem, which says that if you give this set of inputs, you should get this set of outputs.

**1:55** · And what you want to really solve for is how do we solve these competitive programming problems so that-- so the things that we already are able to do as code completions, but when we try to do blocks of code, or solve real problems end-to-end, that starts to be a much harder problem, as you'll see in the ways that this problem gets solved.

**2:17** · So just to give you a preview of how AlphaCode came about and what it achieved, and it was-- this is an older paper, but it's worth remembering that at that point in time, when AlphaCode was released, which is almost four years ago, it ranked top 54% among the contest participants in 10 contests, and this was the first time it was shown that AI can generalize beyond just narrow tasks and solve problems end-to-end.

**2:47** · And this was a much harder problem than what you can do in just human eval, where you basically are given a very small problem like complete this function, or you're given instructions to exactly solve what you want to solve, and you don't have to reason about, understanding the problem and then figuring out what it would take to solve the problem.

**3:06** · So this was definitely longer problem descriptions, longer solution lengths, and you were having to understand from the docstring, what is the right solution approach even before going and solving that?

**3:16** · So it's not just like taking the problem description from the programmer and then just coding it up.

**3:25** · And this is well understood that when the models are generating suggestions in one single line, it's much easier for us as software developers to interact with that, and you get much higher success rates, for example, in Copilot and equivalent functions, but when you have to solve problems end-to-end, that ends up being a much harder problem.

**3:50** · And I'll go through each of these block diagrams one by one.

**3:58** · This is pre having large models, so they actually were pre-training their own models.

**4:02** · The pre-trained models in the next report will get replaced, so what you see here is that you have a stage, where you are basically coming up with a model from which you are going to sample.

**4:12** · Now this model we will later replace with a large language model.

**4:17** · So here, they're also doing pre-training and fine tuning.

**4:21** · And the data that fed that data that really helped this model train was GitHub data and then code contests.

**4:28** · What code contest is basically a large chunk of problems and solutions that come from competitive programming.

**4:35** · So once they trained the model here, they're going to sample a lot of solutions.

**4:43** · So we have seen repeated sampling before, so this is repeated sampling, but at a massive scale, so you will end up with a lot of solutions.

**4:52** · And then you're going to play some tricks to figure out which set of solutions should we even run tests on?

**4:59** · So, so far, we've just been closing the loop, where we take whatever set of solutions the model outputs and then running tests on them.

**5:08** · In this particular case, you're actually going to select, so there's a selection stage before you're going to complete and execute and evaluate.

**5:17** · So just to walk through things step-by-step.

**5:21** · And so the first step is pre-training.

**5:24** · You're going to pre-train a model.

**5:26** · In this particular case, they're going to use masked language model loss.

**5:30** · You can also have a decoder only model, which we'll see shortly, and the model is trained on GitHub code about 700 gigabytes of that trained with next token prediction.

**5:42** · What's interesting is that when they fine tune it, they are using some tricks, so they're using regularization so that they can assign higher probability to more meaningful patterns.

**5:51** · This is interesting in code.

**5:53** · And then they're doing something called as value conditioning and prediction.

**5:58** · So the thing that I want to highlight in this slide is that in the regularization technique, when they're doing fine tuning, they assign higher weight to higher likelihood tokens so that there are certain tokens that will have higher likelihood, and then they are putting lower weight to lower likelihood tokens, so this is called as GOLD, so it will help improve the precision.

**6:17** · So in the next token prediction loss, they are basically adding a weighting mechanism to take into account the likelihood of the tokens also, which helps in certain ways and helps to assign high probabilities to more meaningful patterns, so this is done in the fine tuning phase.

**6:38** · So once you get this model that is able to-- and this was an encoder, decoder model that they were initially using, and then they also tried with decoder only models in AlphaCode 2.

**6:47** · Once they get this model, they are going to try large scale sampling.

**6:52** · They generate 1 million.

**6:55** · 1 million is a large number.

**6:56** · They generate 1 million diverse sample programs per question, so if you have a question, a competitive programming question, they're generating 1 million solutions, half in Python, half in C++, so machines can do that.

**7:09** · And they randomize the problem tags and the ratings in the prompt, and they use a high sampling temperature, so it's like the solutions are going to be diverse.

**7:20** · And once they generate these solutions, what they're doing is they are doing some amount of filtering and clustering.

**7:26** · So they filter the samples to only those that passed tests given in the problem statement, and then they are clustering them so that they're syntactically different, but semantically equivalent, so they differentiate between that.

**7:40** · So they are basically using a clustering mechanism, where they use a separate test input generation model, train it to predict test inputs given problem descriptions, and then create these new test inputs for unseen problems, so they're basically trying to figure out different tricks to cluster this test inputs, the semantic equivalence being one way to do that.

**8:06** · Now the reason this clustering is important is it is effectively providing a way for us to select which set of solutions are diverse enough for us to then evaluate to close the loop.

**8:20** · So now, what you can do is you can submit only a subset of solutions to the Codeforces platform, which is the actual competition platform.

**8:31** · And that will check the program correctness.

**8:33** · It will benchmark against other best performers on this task like human competitors, but the challenge here is that you cannot submit all the solutions.

**8:42** · So 1 million solutions cannot be submitted to this platform, so they have done a curation phase, a filtering and clustering phase to get to this stage.

**8:54** · And then there's also evaluation on code contests.

**8:56** · Remember, that code contest was used to train the model, so there is a test set that they hold out, which will basically give them a signal.

**9:05** · So this is the data set that is created by authors, but they can also measure signal on this particular data set to figure out if their solution is supposed to do well or not.

**9:17** · So when they first did evaluation on Codeforces platform, they took their model, ran it live, generated samples, filtered with example test, cluster to get some submissions, and then submitted it to the platform, and they ran this with-- they submitted in 10 competitions, which each had 5,000 participants.

**9:38** · And what they found was that their solutions with this AlphaCode actually had an average ranking of 54.3, assuming 10 submissions per problem, so not 1 million, and it was competitive with 28% of the competitors in the last six months.

**9:58** · So this table is showing you that if you looked at a certain contest ID, how was the AlphaCode model doing?

**10:05** · What was its percentage ranking, the best ranking and the estimated ranking and the worst ranking relative to other programmers?

**10:13** · This is more of a ranking based as to once you submit a solution, you're ranked based on the efficiency of your solution and the correctness of your solution.

**10:26** · Before I move further, questions?

**10:34** · Yes.

**10:35** · You go back to previous page.

**10:37** · It seems like the-- This one?

**10:40** · So numbers.

**10:41** · In the table, if you look at the performance across different data sets, it seems that-- This is different contexts.

**10:48** · It seems they did pretty well with the final 1623.

**10:52** · Even the worst ones like 54% and 1618 we see the algorithm is pretty good.

**11:01** · But if you look at some others like 1613 and 1615 one is getting worse.

**11:07** · It's getting worse by 20%.

**11:09** · I'm just curious why \[INAUDIBLE\] variation of \[INAUDIBLE\].

**11:17** · I'll ask you that question back.

**11:18** · What do you think?

**11:22** · This is your pipeline.

**11:28** · Where will the variance come from?

**11:31** · So different contexts will have different problem inputs.

**11:35** · Maybe it's the two contexts.

**11:37** · So the two context, they perform well is the context as similar as possible.

**11:44** · But there are other places that \[INAUDIBLE\] somewhere in your context that the algorithm may fail to or struggle to answer because it \[INAUDIBLE\].

**12:01** · The large scale-- so what's your name, again?

**12:08** · What he's asking is why do we get variance across different context IDs, and it does well in one context and does not do well in another?

**12:15** · So at the end of the day, you are depending on how close are these say, contest problems?

**12:23** · In distribution, they are.

**12:25** · So that's one plausible hypothesis.

**12:27** · The other plausible hypothesis is that our ability to-- so in the large scale sampling, that would control like is one of the solutions correct?

**12:36** · But then our ability to select the right set of candidate solutions might also be affected in different context IDs, so the selection stage can also be a bottleneck here.

**12:48** · There can be solutions that are almost correct, but not completely correct.

**12:55** · Yes.

**12:56** · So the \[INAUDIBLE\] example seems like a very arbitrary one.

**13:00** · Do you have an experiment that shows how the model possibly scales as the number of samples?

**13:08** · So I think you're basically right.

**13:10** · So they do have some experiments that they did, but it's order of magnitude.

**13:15** · So with this particular model size, and there is some results I'll show you.

**13:19** · With this particular model size, they had to go for much larger number of samples.

**13:24** · If you remember from earlier slides on test time compute, when you have smaller models, you do have to go for much larger number of samples to get the same pass@k.

**13:35** · For example, here is one of the saturates, because-- So let's look at the results and then come back to that comment.

**13:43** · But on the question around why is it different in different contexts?

**13:47** · The inputs are different and then the pipeline will-- the selection stage can be a bottleneck, so both of those influence where it does well and where it doesn't do well.

**14:01** · So there is two things worth noticing.

**14:04** · So when we compute solutions with repetitive sampling in test-time compute, and this is something that you're definitely using in homework two, you have this notion of pass@k.

**14:16** · So that's the percentage of problems.

**14:18** · So if you get the model to generate k samples and you submit all of them for evaluation on the hidden test, how many problems will actually solve the problem description that was given?

**14:31** · It measures how good is the search aspect of the sampling process, so it's basically coverage in the lectures that we covered before.

**14:39** · What this particular benchmark measures is 10@k.

**14:45** · 10 being the number of submissions that you're going to go submit for evaluation.

**14:50** · So even if you get the model to output k samples, in this particular case, 1 million, you don't have the ability to measure correctness on all the samples for the final set of solutions, so you do have to do some selection, or scoring to decide which set of solutions I'm going to submit.

**15:09** · So it measures also the filtering process of how well the model will behave when you have a very large number of samples, so you're not just generating samples, but you have to do some search yourself before you can submit the solutions for evaluation to hidden tasks.

**15:26** · Now, why does this matter?

**15:28** · So this is validation set and that's test set.

**15:32** · And they train different model sizes, so this is 9B model, 41B model, so that's a larger model, and then 41B with clustering.

**15:41** · And what they're presenting is validation set results for 10@1k, so this is the question you were asking me.

**15:51** · They're basically going to submit 10 solutions out of 1k generated outputs, and then keep increasing that to 10k, 100k, and 1 million.

**16:00** · And then they're going to do similar set for test set as well.

**16:06** · And what you will notice is that typically, the larger model size consistently will do better than the smaller model size.

**16:13** · That is something we have talked about before.

**16:16** · But the other thing to notice is that as you go for larger number of samples, which is something we have seen as well, you are able to do better.

**16:24** · So going from 10@1k to 10@1 million, you're clearly doing better, and same on the test set side.

**16:31** · And the clustering.

**16:33** · So typically, we had covered this slide with pass@ number of samples.

**16:40** · In this particular case, even clustering is consistently-- so 10@1k will definitely also improve similar to pass@1k.

**16:50** · And then if you look at the last row here, which is 41B plus clustering, you see that that's consistently better.

**16:56** · So like 9B, versus 41B, versus 41B plus clustering.

**17:00** · The 41B plus clustering is definitely going to still be better than the one before because it definitely provides an improvement.

**17:09** · And the reason for doing that is because if you were to measure the set of solutions that the model has output and you wanted to measure their diversity, the clustering provides you a way to submit only the diverse set of solutions, if you can only submit 10 problems.

**17:24** · And since competitive coding problems are quite difficult, you don't get much benefit out of submitting the same set of solutions to the evaluation process, so if you can choose which set of problems to submit, that helps.

**17:42** · And if we were to measure just 10@k and pass@k, if you had-- so pass@k would be unlimited attempts and 10@k would be 10 attempts on evaluating per problem.

**17:55** · On the x-axis, you have the sampling budget, and on the y-axis, you have this accuracy in terms of how many attempts you get to solve the problem.

**18:06** · The solve rate definitely scales linearly with more samples, so this is very much in line with what we had seen for pass@k in repeated sampling.

**18:14** · So even after the selection stage, we definitely see the same log linear trend with more samples.

**18:20** · And better models have better slopes, so this particular case, you see the 41B, which is the blue curve, has better solve-- Sorry, the purple curve, 41B, has better slope compared to the 300 million parameter model at the bottom, and same applies even for pass@k.

**18:38** · And then the final thing is that when only 10 samples are submitted, then you do get bottlenecked in certain ways, so you can get higher accuracy.

**18:51** · So if you compare the y-axis 10@k versus pass@k, if you have unlimited attempts per problem, which is a synthetic scenario, you are almost getting to something above 40%, and here, you are only getting to 30%, so there is definitely some bottlenecking happening in selection stage.

**19:09** · So you are bottlenecked by how you filter and cluster in some ways, when you have to choose which set of solutions will pass the test.

**19:21** · Yes.

**19:23** · I'm just wondering if this trend continue, you really got this tool another six or more.

**19:31** · That would be 1 trillion.

**19:32** · If you really get 1 trillion as the score, this attracting demo will be double.

**19:37** · So I think that we really need to just make it 1 trillion.

**19:43** · We can just double the performance.

**19:47** · Well, we're going to AlphaCode 2.

**19:49** · Making the model better is a slightly easier access than scaling the number of samples that you're going after.

**19:55** · So on AlphaCode 2, the model performance improves, and that helps you reduce the number of samples to get the same performance or at 1 million, you'll get a much better performance.

**20:05** · So this is an older model, but it's a weaker model.

**20:08** · But the trends generally hold.

**20:12** · And in some ways, there a-- I mean, the larger models have done better generally speaking, but there's a model capability gap.

**20:21** · So if the base models are not strong enough, they're going to hit limits at a certain point.

**20:27** · So the problem is if you really have no problem with the sample budget.

**20:30** · So you can really be confident in the whole purpose, or you can just really do one bit of a three example with this graph.

**20:40** · If the log linear trend continues then yes.

**20:43** · That might be a project idea worth exploring if the costs are not prohibitive.

**20:54** · Yes.

**20:55** · I just want to say I think that could be really useful if you think that one problem is really important.

**20:59** · You can just forward your-- All you can do is solving that problem.

**21:03** · According too, yeah.

**21:06** · I think the challenge for that, which is something that is worth also-- that's a good comment.

**21:12** · So one of the challenges with solving it that way is that you kind of assume that if we sample more, the diversity continues to increase.

**21:22** · So one of the challenges that we will see in AlphaGo 2, and I'll emphasize again, is that you do have to ensure that as you sample more and more, you are getting more diverse solutions.

**21:31** · And part of the process of clustering is that it's effectively figuring out which are the diverse set of solutions.

**21:37** · So if you sample 10x more than what was sampled here, that you don't end up with more diverse solutions, then you're actually not going to improve.

**21:46** · Is there a reason why we have a log linear relationship here?

**21:50** · Why is it not any other modeling of y versus x?

**21:55** · So this was covered earlier, I think the passer k versus unlimited attempts.

**22:00** · This is theoretically derivable.

**22:03** · And I think the main thing that I'm emphasizing is that even after the selection phase, that log linear trend holds.

**22:10** · The passer k versus sample budget, this was covered in-- I don't know the lecture number, but Azalea covered this in that paper actually theoretically derives it.

**22:19** · This is the large language monkey's paper or the one right after that.

**22:24** · Yeah, but if you look at the derivation, we can work through that offline.

**22:36** · OK, So if we look at takeaways, I think the fun aspect here is that we can get high coverage by sampling, and then-- so this large-scale sampling, this filtering, and the clustering approach, you can get higher coverage.

**22:52** · And they were able to actually also make sure that the model is not just copying existing solutions.

**22:59** · It actually reasons.

**23:00** · So they did some search over the training data and actually saw that there was-- the generated code had some novelty.

**23:06** · So this was actually generalization out of distribution.

**23:10** · The challenge with these particular set of approaches that they noticed that's worth highlighting is that they were training the model on loss.

**23:17** · And loss is often a poor proxy for solve rates, so because there are many solutions that could have solved the problem.

**23:24** · So they did see that this model did not do well on say, dynamic programming or constructive algorithms in some ways.

**23:31** · So it was not the strong in certain domains.

**23:35** · And then the other aspect was that it was requiring a large-scale set of sampling.

**23:40** · So that was not ideal in terms of how practical this is to be used everywhere.

**23:48** · If there was a time bound, then you can imagine.

**23:54** · So if you basically were just examining accuracy, then you want to make unlimited attempts.

**23:59** · But if you want to do time-limited bound in terms of efficiency, then you do want to rank acceptable solutions as they get generated.

**24:08** · So that becomes really important.

**24:10** · And as I already mentioned, the more difficult domains required more experiments.

**24:16** · So this was not like-- this solution approach actually wasn't working well on difficult problems.

**24:22** · And in fact, there, it's both a matter of you might need more steps to solve the problem.

**24:28** · So this particular approach in one shot did not do a reasonably strong job.

**24:32** · So multi-step solution approaches would do better here.

**24:38** · So this was AlphaCode summary.

**24:41** · Now, let's see.

**24:42** · What can we do better?

**24:43** · So this was like 2022.

**24:45** · If you look at the next set of paper which is AlphaCode 2, they improved upon this substantially.

**24:50** · And that was really helpful.

**24:53** · And we can also learn what were the differences.

**24:57** · And that really helps us understand what pushes the frontier even further.

**25:01** · So AlphaCode 2 started with a hypothesis of what if you don't pre-train your model?

**25:06** · You use an existing LLM.

**25:08** · So in this particular case, this work was at Google.

**25:10** · So they decided to use Gemini Pro instead of using in training their own model.

**25:18** · And then, they want to customize it to get a better performance on this particular problem set on competitive programming.

**25:27** · So the first set of changes that were made were that instead of pre-training, you basically are just going to fine tune Gemini Pro.

**25:33** · So it's not just prompting.

**25:35** · They are fine tuning the model.

**25:36** · And then, in terms of sampling and evaluation for the large-scale sampling, they want to ensure diversity.

**25:43** · So for diversity, they actually had multiple AlphaGo 2 models that allow for massive sampling.

**25:49** · So when they did and go and do fine tuning, they actually had multiple variants of this model so that they get diversity in the output sampling.

**25:58** · And then the third thing they did was that to select the subset of candidates, they had a scoring model.

**26:04** · So you can see that as a reward model, which was used for obtaining the best candidates.

**26:11** · So it's not just based on clustering and filtering, which is a heuristic for saying OK, this would be semantically equivalent, but there's diversity in syntax.

**26:24** · They are actually now going for a scoring function which can learn that function.

**26:29** · So it's a learned approximation of what should be given high score and what should be given low score.

**26:36** · So the new ideas here, as I highlighted, was A, that they are going to fine-tune a Gemini Pro model to score correctness before submitting.

**26:46** · So that's a reward model.

**26:48** · And they also had a family of models based on different hyperparameters, so different difficulty levels, different tags.

**26:55** · So they fine-tune several models with varied hyperparameters, and then that maximizes the diversity of the number of samples they generate.

**27:02** · And they also improve their data sets.

**27:04** · So the data set that they fine-tune on is V2 version of CodeContests, which is actually open source.

**27:10** · And then, they had another high-quality data set for scoring purposes.

**27:16** · So going back to this diagram, what changes next?

**27:21** · So let's take a more detailed look.

**27:24** · So here, if you look at the input model on the fine-tuning stage, you have this new data set called CodeContests V2, which is going to be used to generate.

**27:38** · Now, you're going to do some tagging.

**27:39** · So there's some amount just like, take your CodeContests V2 data set and put-- bisect it or rather segment it into different data sets to fine-tune different versions of models that are going to generate samples.

**27:53** · So that's one set of intermediate AlphaCode 2 models that they will generate.

**27:58** · And then they had another high-quality data set they're going to use to make this even better.

**28:02** · And this same set of model, same set of data will also be used to generate a scoring model from the same model.

**28:10** · And based on that, they're going to-- so this is basically a notion of the zero.

**28:16** · The data set is segmented and used to tune multiple models to get more diverse samples.

**28:25** · What's different about the data set is that the problems and solutions are higher quality and vetted and scored better.

**28:32** · And the scoring model is able to estimate the correctness of the code sample between 0 and 1 based on this higher quality data set.

**28:41** · So they manually curate it.

**28:44** · This data set got more human annotators in place so that they could train the model to estimate correctness better.

**28:54** · And then the other aspect is that they had this family of models instead of having just one model.

**29:00** · Now, on the sampling and evaluation side, they split the sampling across models.

**29:08** · They in fact, went to only C++.

**29:10** · Earlier it was C++ and Python half samples.

**29:13** · So they split the sampling across models but only C++.

**29:16** · And when they generate the samples, they're randomizing the temperature and the metadata so that they can get diverse outputs.

**29:23** · So this is the massive sampling pipeline.

**29:27** · For each output, they're going to execute on test input, and they are filtering out anything that's incorrect or doesn't compile.

**29:34** · So they remove 95% of the samples.

**29:36** · At this point, they're left with about 50 case samples.

**29:39** · And then, after that process, they're going to aggregate and keep the top 10 largest clusters.

**29:46** · There's reranking on top of that based on the scoring model to say how likely is it to be correct.

**29:53** · So they score each code sample and pick the best candidate per cluster.

**29:58** · And once they have that, that's when they're going to submit and say that did it win or did it not win?

**30:04** · The eval is going to be same as AlphaCode.

**30:07** · So if we are to compare results now, this is comparing AlphaCode 2 versus AlphaCode.

**30:13** · So AlphaCode-- so on the x-axis, you see the sampling budget.

**30:19** · AlphaCode, we were doing 1 million samples.

**30:21** · Here, we are going to vary the sampling budget per problem.

**30:25** · And on the y-axis, you have solve rate.

**30:29** · As you can see that, once you get to 100 samples, you basically-- so AlphaCode was using 1 million samples.

**30:36** · For AlphaCode 2, once you get to 100 samples, you are achieving the same solve rate as AlphaCode.

**30:43** · And if you want to go beyond that, you can use more samples.

**30:47** · So the solve rate is still improving with the increase in sampling budget.

**30:51** · And if you were to basically say, what is the maximum performance achieved?

**30:56** · AlphaCode 2 with 1 million was solving 43%.

**31:01** · It was getting 43% solve rate, while AlphaCode was only getting 25%.

**31:05** · So in this particular case, even though there is using the same number of samples, a better base model, better diverse solutions, and then better scoring is giving them.

**31:16** · So this whole system is giving them performance gains, which is almost 2x relative to where the previous system was.

**31:27** · Questions?

**31:31** · Yes.

**31:34** · 95% of sampling wasted on not compiling or a poor answer seems like a very high cost.

**31:42** · Were there any other studies to see if there could be better methods of sampling, more reliable answers, maybe really better prompting, or-- I mean, it didn't mention randomized temperature, but were there any other approaches?

**31:57** · So in this particular case, this paper did not.

**32:00** · But if you are to refer to some of the work that we have discussed before, what would you need to do to improve that?

**32:09** · This is an older piece of work, right?

**32:11** · Yes.

**32:12** · I would try the approaches we took in homework 1.

**32:18** · Like?

**32:19** · Like better prompting or better-- maybe using-- instead of wasting all of the compute on 1 million sample, maybe I would try to self-iterate based on one of the sampling at least once or maybe at least try to have a better method of aggregating some of the information from the various sampling.

**32:38** · Great.

**32:39** · So I think what you're saying-- so just to repeat the answer, in homework 1, you had done some form of self-refinement.

**32:46** · So this is essentially parallel search, in some ways.

**32:48** · You've generated a lot of solutions, and then you are clustering on top of that.

**32:53** · If you do a refinement process where you have generated some solutions and then you're saying, OK, if I can get any feedback on top, then can I improve these solutions better?

**33:02** · That's one approach that would cut down the number of samples, but increase the time that if you can collect any feedback.

**33:10** · The question I would ask is that how would you collect feedback?

**33:12** · Like, what would be feedback in this particular case?

**33:15** · That's worth thinking through.

**33:18** · I think the other comment would be that if you can get the model to do slightly better with RL, so if it can get better at solving things with the RL loop in between when we cover train time scaling, then that can help cut down how much we need to put in test time.

**33:36** · So both those approaches can reduce the cost on the sampling side.

**33:46** · Let's try that one.

**33:48** · So when it comes to a practical application-- so when we are using everyday thinking models and we are still talking about a couple of dozens of samples, I mean when it comes to time scale, and when we hear about these OpenAI authenticate a month's researcher, those are the multi thousand, multi hundreds of case of samples applied in production.

**34:17** · So I think the way to look at the system is more of how you would build a system that is generating those dozen of samples.

**34:25** · I think we have discussed this before.

**34:28** · For us to think about these systems, I think the big question you're asking is how would you build the system to begin with that can reason well, that can close the loop?

**34:40** · So I think there is a line of research which has tried to answer that question.

**34:45** · And what this is covering is that if you started with an LLM and you wanted to solve these complex problems, how would you build a system that can solve that problem?

**34:54** · And then, if you can distill all of that knowledge into a single model, then that becomes a large reasoning model.

**35:00** · But this is more of a multi-agent system in almost some ways, where you're basically having one model produce outputs and then another model score it.

**35:11** · And then, here a family of models is producing outputs, and then there is another family of models that's scoring it.

**35:17** · So that gives you more tricks up your sleeve if you had to re-architect the system from scratch, as opposed to depending on what the current generation of models can or cannot do.

**35:28** · And the paradigm, I believe, because at the end of the day, when we are saying in test-time compute, there should be a solution in this space of what model outputs generated, the paradigm is effectively that you should be able to search that solution.

**35:42** · So what this is roughly answering is how would you search for a solution in the output space of what models output?

**35:54** · You still have question?

**35:55** · Yes.

**35:57** · So why is the scoring model here?

**36:01** · Nothing is a suppose gift.

**36:03** · Say that again.

**36:04** · Why is the scoring model-- I think the value is called-- how am I saying this?

**36:10** · Why is it called-- why is the scoring model only desired model use?

**36:15** · So I think the way to look at it is that why is the scoring model not using code count as V2?

**36:20** · I mean, you can train your-- so the code counts as V2, there would be contamination, right?

**36:26** · The scoring model should not see exactly the same data, but it does need to see some data in the distribution, right?

**36:33** · It's basically a matter of you're training the scoring model, not necessarily on the same problems, but you want this-- if you're designing that system from scratch, how would you train a reward model?

**36:43** · Would you you want to show it is that for these kind of problems, if you had these two solutions, which solution should you prefer?

**36:50** · That's what you're teaching the scoring model or what ranking should you apply to that?

**36:57** · And if your first train-- well, that is you on budget.

**37:00** · So the first train is that kind of model that you have to decide.

**37:03** · Is it the same, for example the two legal set that it were?

**37:11** · I mean, you could have mixed those data sets and then done the same thing, yes.

**37:16** · But that is a doable exercise.

**37:18** · It's just multi-stage.

**37:21** · It's not the same in the sense that when you do any kind of fine-tuning, if you're changing the quality, then the model-- and if you're not mixing the previous version, then the model is forgetting some of the previous information when it's tuning in the last stage.

**37:39** · OK?

**37:46** · So if you were to look at the aggregate results of AlphaCode 2 in terms of the normalized score versus the how it would compare to human contestants, there.

**37:59** · And the way you would do that is you would basically compare the percentile of contestants who score at a certain level.

**38:06** · What AlphaCode two was achieving is 85th percentile between the expert and the candidate or the master candidate solutions, while the human-- While AlphaCode was outperforming, 46% AlphaCode 2, if you took top two performance on the-- if you took top two solutions, then it was actually outperforming 99.5%, but overall, it was basically scoring closer to 85th percentile across human contestants.

**38:35** · So that was a big deal.

**38:36** · It was like, OK, in this particular code, these problems and this competitive programming, it's doing very well in some way.

**38:43** · So that was a big accomplishment in one single year just with an improved system.

**38:51** · And I think, for us, what's worth learning here is that we are increasing the performance with less number of samples.

**38:58** · So we didn't have to necessarily scale the number of samples.

**39:02** · But we had better foundation model.

**39:04** · And then the scoring model that is selecting the best candidate is also helping the solution.

**39:10** · The experimentation is still quite costly.

**39:12** · And then, as one of our classmates pointed out, this is very specific to code.

**39:18** · And then a lot of the compute is wasted in generating samples that might have bad syntax and so on that you have to go and filter out.

**39:25** · So one set of questions that I have for the class at this point in time is that how would you change these methods based on task complexity, for example?

**39:39** · So actually, I will pose that question.

**39:42** · And then the other question I will pose is, how can we embed reasoning directly into these models?

**39:48** · Take a minute to talk to folks next to you or somewhere in the vicinity.

**39:54** · And then let's come back and discuss those two questions.

**40:01** · Let's tackle the second question.

**40:03** · So how can we change these methods based on task complexity?

**40:06** · So if I have easy problems versus hard problems.

**40:10** · Any takers for that?

**40:20** · OK.

**40:20** · What you could do is you have a separate model initially judge each question based of it.

**40:27** · It would made easy, medium, or hard.

**40:29** · And you create, like your data set where you're sampling from also has those labels.

**40:33** · Then in this, if you declare a question that's easy, you sample more from the easy bank.

**40:38** · So it's a better sample you can struggle with.

**40:41** · So is it more on the training side you will change or is it more on the sampling side that you'll make this change?

**40:46** · More on the sampling side.

**40:48** · That's where you will change.

**40:49** · There isn't more-- you can root any more of this.

**40:52** · OK, so you're saying that if you have a simple problem, then you will sample more from-- --the simple problems, yeah.

**41:03** · OK.

**41:05** · So you will-- in AlphaCode 2 basically, you will use the model that's trained on perhaps simpler problems.

**41:10** · Is that the suggestion?

**41:11** · OK.

**41:14** · Are there ideas?

**41:19** · The solver did improve with model size.

**41:21** · That's-- What if you can identify a simpler problem, maybe you can run with less samples.

**41:37** · Yes, exactly.

**41:38** · So if the model-- so this is something that was probably seen in the repetitive sampling and the test-time compute as well, is to-- if you have simpler problems, then it's likely that you can get coverage with fewer number of samples.

**41:51** · So you don't have to go to 1 million samples every single time.

**41:54** · It's almost like saying the model does-- more likely to generate the solution in the search space of what it outputs.

**42:03** · So it should be easier to sample or its initial set of solutions with some iteration, with some iterative refinement should be easier to correct, as opposed to having to generate a lot of different solutions.

**42:18** · One of the gains that you get if you generate a lot of parallel solutions is that you're trying to get the model to provide diversity in the approaches, and you're not trying to get it to fix what it already output.

**42:35** · What about the question four?

**42:37** · How can we embed reasoning directly into the model?

**42:43** · OK, let's try out.

**42:45** · Let's see what you already said.

**42:46** · Maybe you can have more on the training side.

**42:49** · By dealing with the training side, you can take all the comments off.

**42:53** · You've done enough problems so you know in the second one how it already feels after, like the framework of the solution.

**43:00** · Instead of one, you know it's very probably to the problems that we mentioned in that framework.

**43:05** · And that is slightly-- it's slightly different than the standard of directly for when solving being the change or we'll be solving.

**43:13** · We have the final solution and the bit of the final solution.

**43:16** · So if we don't have enough common data, then we use the LLM to test if there's a code to see the first section is about what, the second section is about what, the third section about what.

**43:28** · So it's-- the training data is that part of the training.

**43:32** · The data is only the framework, the set where it's that few steps with that form under that pre-training and that space between the same.

**43:41** · OK.

**43:42** · So what Geoffrey is saying is that you add hints in your training data set around the solution of what kind of algorithm is being used to solve the problem.

**43:50** · What's a more generic version of that?

**43:53** · What have we already covered in that line of work?

**43:59** · As programmers, you think before you write the answer.

**44:03** · What if that thinking could be captured?

**44:08** · If you added those chain of thought as part of your training set or if you remember the STAR approach where you're getting the model to generate the solution and then give the hint as the answer and then ask it to come up with that reasoning, then that can also be part of how the model embeds it, right?

**44:31** · Any other ideas?

**44:35** · I think the other interesting thing that was mentioned, which is probably worth highlighting, is that if you have a more complex problem than you might want to decompose the problem into subparts and add hints for subparts as opposed to trying to solve the problem in one go, because these are hard problems.

**44:57** · Yes.

**44:58** · It's about what you tackled that for the standalone but that's sequential.

**45:01** · Maybe you give-- you succeed on the first intermediate output, and you have something forward that is never going to make the second part work.

**45:10** · So how does that sequential or how can you decompose that work?

**45:15** · So I think all of these are hinting at we do need to close the loop at some point in a multi-step fashion and almost want a tree search style of solution where you basically want the-- I basically sample for, say, the first step, and is that roughly correct?

**45:32** · And you want to sample for the second step, and then you want to be able to backtrack.

**45:36** · So it's roughly heading in that direction, but it's early work that gives you hints.

**45:44** · So it's basically got on your thinking, and then perhaps that's your project, right?

**45:48** · But your question is very relevant as to what happens if your answer is correct in the first step, but then the next step is not correct?

**45:59** · And the task decomposition is often relevant in that most problems have a certain way of solving.

**46:06** · So if there is common instructed patterns, then that's doable.

**46:09** · But if you do expect patterns that are out of distribution, then maybe, you do need human in the loop.

**46:18** · That's like a scientist style of work that folks covered last lecture.

**46:31** · OK?

**46:32** · OK?

**46:33** · Let's come to the last part.

**46:35** · So we spent a lot of time on just code and how to select a set of code samples that can pass and solve competitive coding problems.

**46:49** · Now, let's look at how would you do something like building a deep research agent?

**46:55** · So Search-o1 is basically going to use large reasoning models as the base and then try to build a deep research agents on top of that.

**47:03** · And it's worth paying attention because you will use this in homework 3.

**47:08** · So the key idea here is that you want to use large reasoning models to retrieve based on a query that you want to give the model.

**47:16** · So large reasoning models have impressive reasoning, but as you know that most of these models are trained on with some knowledge cut off dates, so they typically will not have the freshest knowledge.

**47:28** · If something happened yesterday, the model will need to go look up that data.

**47:32** · It's not going to be there in the model.

**47:36** · The other challenge when you work with reasoning models, per se, is that they will go and output a lot of tokens in long-form reasoning, but when they have knowledge gaps, they will be using terms that are expressing uncertainty.

**47:51** · So one example is that if you go use benchmark on GPQA data set, you will see the term perhaps in the reasoning chains a lot, or you will see the term alternatively or wait or-- so they're basically expressing that the knowledge gaps will show up as uncertainty in the way the model is thinking.

**48:13** · So you want to bootstrap that in some way, because otherwise, those knowledge gaps will continue to propagate through the entire reasoning chain.

**48:21** · Now, one simple solution based on learning from feedback or learning from tool calls is that why don't we just take this query and get a relevant document?

**48:32** · So you take this query, pass it to a search tool, and get the relevant document, and then put that document in the prompt, and then get the model to output based on that.

**48:43** · Why is that not enough?

**48:44** · So that would be more like retrieval augmented generation.

**48:47** · So whatever is your question, you generate a query, and you get a document, and you put it in the prompt, and then that's what you use to retrieve the answer.

**48:58** · Now, the challenge with that sort of simple approach is that you retrieve once at the beginning.

**49:04** · So you don't have the ability to tweak things.

**49:06** · And it's possible that if your search problem is complex enough, then each reasoning step will need different pieces of information.

**49:15** · So if you have a problem, which is asking just the weather, then maybe a single search call is enough, but if you're asking to solve a complex problem, which has multiple parts to solving it, then after it gets through a certain amount of reasoning, it needs to go look up additional information.

**49:31** · So for complex reasoning, it's extremely hard to get it right, and same for multi-step reasoning.

**49:36** · So typically, retrieval augmented generation will improve-- will show improvement over direct reasoning, but in multi-step reasoning, it definitely suffers.

**49:46** · So the solution that Search-o1 proposes is that the model generates the queries on the go.

**49:55** · So whenever it sees these knowledge gaps, it will trigger a query.

**49:59** · It will generate a search query of what tool calls to generate and go search things over.

**50:07** · And there will be multiple iterations in a single reasoning session of like fetching these documents.

**50:12** · And the second thing it will do differently, and I will show examples of that, is that it will analyze the retrieved documents.

**50:19** · So instead of just dumping what it retrieved as the document, it will analyze the retrieved document and extract relevant chunks of information from there.

**50:28** · And it will only put these relevant information into the prompts so that it integrates well into the reasoning chain.

**50:40** · So just to reiterate how this works-- so this is an original question, which is a chemistry question, which is talking about-- it wants to get the carbon atoms count of product 3 which is output of a bunch of different chemical reactions.

**50:56** · So if you were to use a large reasoning model, you would ask the model to start thinking.

**51:01** · It looks at this term, which I don't understand, and perhaps the model doesn't understand.

**51:06** · So it will go ask a lookup, what does it mean?

**51:10** · Now, one trick is that it doesn't go look up, so it makes a guess and comes up with whatever is in its knowledge base in the stored weights and provides a final answer based on what it guessed.

**51:21** · But if there is a guess here, and it got the answer wrong, then those things will cascade as errors into whatever is the final answer.

**51:28** · So all the perhaps or all the uncertainty will basically cascade into the final answer.

**51:33** · So your certainty for the final answer is low.

**51:37** · Now, one possibility is that you basically-- whenever you encounter unfamiliar knowledge, you can now do web searches.

**51:42** · So that would be a simple scenario of like OK, unfamiliar term, basically go and do a tool call for search, return the document that basically has that search tool for perhaps there is a Wikipedia page, or there's a web page that has that information, and put that in the reasoning chain, and now do the-- put that in the prompt, and then do the call again, and then provide the final answer based on that.

**52:08** · The only challenge with this is that as you basically increase your amount of content you're putting there, there might be not as much relevant content in these documents.

**52:19** · Like if you went and fetched like 10 documents that were related to the information, there's too much information for the model to process, so it might actually not still give the correct answer.

**52:28** · So in this particular case, it was like 10 carbon atoms in product 3.

**52:33** · Here's 14 carbon atoms.

**52:34** · So it still got it wrong.

**52:38** · What Search-o1 is proposing is that now you have-- whenever you get the unfamiliar knowledge, it will go and search for helpful information.

**52:47** · So that's still a tool call to your search.

**52:50** · But then, it will reason within the document.

**52:53** · So it will try to look at these documents and see if this is helpful information or not, extract the relevant content, and then put it back in the next prompt, like what is the relevant chunk of information to put?

**53:06** · And that will allow the model to continue coherent reasoning and provide the final answer here.

**53:11** · So in this particular case, basically, the ability to do this summarization of information or reason within the document really improves the quality of life, how it gets to the final answer instead of clustering the prompt with 10 documents or 20 documents.

**53:29** · Questions on what's the difference between the three approaches?

**53:36** · Yes.

**53:37** · Why in the final leg there does it say-- in the first one, it says-- or perhaps, it may look at as far as this little one.

**53:44** · Does it concern you?

**53:46** · Because it's been given the information.

**53:48** · So the uncertainty has reduced.

**53:50** · It has actually been-- it's not even saying that in the middle one, which-- because it's been given the right information in the prompt.

**53:59** · I think the harder part is, how does it know what to search for?

**54:05** · It needs to know which keywords it does not know.

**54:12** · That's the question I would ask.

**54:15** · It gets to know his answer.

**54:17** · The answer is I think you basically need to break down what are the key-- so there is different ways to tackle that question, right?

**54:25** · If you're building a real application, you want to identify which parts-- you don't want to rely on the knowledge base of the LLM.

**54:34** · And you actually do want to do a tool call because that information is likely not what you want to trust the weights of the LLM for.

**54:43** · It's almost like you're finding the key entities in your question and fetching information on those.

**54:59** · OK.

**55:00** · So there were two things that we are covering here.

**55:02** · So one is the Agentic RAG, and one is Search-o1.

**55:05** · So I'll cover both here.

**55:07** · Let's first understand Agentic RAG because then, we build on top of that in the Search-o1 process.

**55:13** · In Agentic RAG, what you're doing is you're basically-- every time you are hitting entities that you care about, you're basically going to insert special tokens where you are going to trigger a search.

**55:25** · And then when you get that document, you're going to insert those results.

**55:29** · So model is generating some output tokens.

**55:32** · When it's seeing certain amount of uncertainty in its output tokens, it's generating these search queries between the special tokens.

**55:39** · And based on that, it goes and does the tool call.

**55:41** · And the retrieval tool will essentially return those documents, which will then be inserted into the reasoning chain.

**55:47** · So this is happening in large reasoning models as part of the whole reasoning process of like, it's also calling tools as part of the reasoning process.

**55:56** · So that's one way to solve it.

**56:01** · But the documents can be lengthy, and they can contain noise.

**56:05** · And oftentimes, depending on how good the long-context understanding and reasoning of the model is, they might-- actually, if you put 10 or 20 documents, it might actually not be able to do a good job at reasoning over them.

**56:16** · So the reason in documents module of Search-o1 will allow you to do analysis of each of the documents of how relevant the content is, and then it considers the current query, what it was reasoning previously plus this chunk of information that it extracted, and appends that to the prompt to allow the model to continue reasoning based on that.

**56:39** · So it's essentially a multi-step process within that retrieval tool function itself because it's basically getting that document information, but then also doing an extraction process on top of that.

**56:50** · It's as almost as humans.

**56:52** · You don't want to just go and curate all the possible references.

**56:56** · You also want to take notes on those references so that you have some way of doing a better job understanding and synthesizing that information.

**57:04** · And this allows the model to do a better job at reasoning when we are adding external knowledge.

**57:10** · And especially for complex queries, this becomes quite important.

**57:14** · Yes.

**57:15** · How is it pausing previous reasoning?

**57:18** · And if there's any corrections needed for the previous reasoning, how does it handle corrections?

**57:23** · So there is an assumption that there is a state or there is a memory buffer that's keeping that.

**57:30** · It's not obvious in the way this is structured, but there is basically some form of notion of this is the search query I'm trying to answer and some buffer of where is the previous reasoning and so on.

**57:43** · All of it in the slide.

**57:44** · Yeah.

**57:46** · Yes.

**57:47** · \[INAUDIBLE\] to prepare some new form in the Agentic RAG module.

**57:53** · On top of that, we just ask the model to do some summation and then it continues reasoning.

**57:59** · So is that directly transferred to the second style like-- I mean, does this directly mix method to be the new method proposed when it's due?

**58:17** · Say that part again, or you can just speak up louder.

**58:21** · I mean, if you just modify the prompt in the Agentic RAG module, like you ask the model to do some summation and then continue the reasoning, does that produce the same result on recent models?

**58:37** · So I think that's a great question.

**58:39** · And I would encourage you folks to actually try that out in homework 3.

**58:43** · I think the assumption there is that if you were to issue that prompt, you are assuming that the context length of the model and the reasoning over that context length is working really well.

**58:55** · This is basically Agentic Context Engineering-style paper.

**58:59** · So it's basically-- there's a recent paper called "Agentic Context Engineering."

**59:03** · So essentially, the limitation here is coming from what can you put in context length that the model is going to do a really good job at.

**59:13** · In ideal world, we would want that.

**59:15** · That's where we want to shoot.

**59:17** · And hopefully, by the end of the year, that's where we will be.

**59:22** · OK.

**59:23** · So let's look at the example.

**59:25** · So we were covering this example of carbon atom count in product 3 based on a bunch of different chemical reactions.

**59:31** · In vanilla reasoning, the challenge was that it was guessing the structure.

**59:35** · So it definitely got wrong answer.

**59:37** · In Agentic RAG, because you were just retrieving the documents, they ended up being too lengthy, so it did disrupt the reasoning.

**59:44** · In Search-o1 process, it did search for this particular formula, and then it refined it to a certain structure, and then that integrated cleanly into reasoning.

**59:55** · So essentially, the notion of extracting the right information from the documents really helps Search-o1 and get to the correct answer in this particular case.

**1:00:07** · Now, if you were to go beyond the example to results, what we're plotting is different domains, physics, chemistry, biology, and overall.

**1:00:14** · And you're plotting pass at 1 on the y-axis, and then you're plotting the number of documents that you get on x-axis.

**1:00:25** · So typically, as you increase the number of documents, for direct reasoning and for RAG, the accuracy does not go up.

**1:00:33** · But in this particular case, as you increase the number of documents, you are actually able to do better because you can summarize what is relevant information or not, in this particular case, assuming that the documents-- fetching more documents gives you more relevant information related to the problem that you're solving.

**1:00:51** · So this is basically another axes of-- instead of doing iterative refinement, you can do parallel refinement because you can basically go fetch more information and then chunk it down to put it in the model context.

**1:01:05** · Now, if you were to compare the performance on GPQA data set-- so if you just compared GPQA data set in physics, chemistry, and biology-- I was showing you a plot in the last slide-- human experts in physics, chemistry, and biology on GPQA would score this much.

**1:01:25** · If you look at the reasoning models and you build Search-o1 and on top of them, what you notice is that-- for example, in physics and chemistry, Search-o1 actually is quite competitive, sometimes even better than what human experts would do.

**1:01:42** · These are hard problems, by the way.

**1:01:45** · And in biology, it's almost competitive to say the biology is solving the problem.

**1:01:52** · One comment I want to make is that you want to focus on physicists solving physics problems.

**1:01:57** · So you want to focus on the diagonal here.

**1:01:59** · It's maybe not obvious like if you change the domain then.

**1:02:03** · That's the number you're comparing to.

**1:02:05** · So the Search-o1 is doing pretty well in physics here and in biology here, and in chemistry, not so much.

**1:02:15** · \[INAUDIBLE\] this Search-o1 perform even better than most physicists do this.

**1:02:24** · So what's the level of this physicists?

**1:02:26** · \[CHUCKLES\] Maybe they didn't do a good job sourcing the physicists.

**1:02:33** · I think we're definitely getting to a point where the models are able to do well in certain domains more than the-- but this is not to say that you're outperforming human experts.

**1:02:44** · It's more to say that you're competitive with the human experts for this class of problems, yeah.

**1:02:51** · So there's still a lot of headroom in chemistry.

**1:02:54** · \[CHUCKLES\] Yes.

**1:02:57** · I have a question for the chemistry.

**1:02:59** · You've seen a lot even all this chemistry like the-- what's so fetching we should-- chemistry formula can be wrong.

**1:03:06** · I'm just wondering whether it performed worse in the chemistry just because the chemistry part, how to organize it is complicated.

**1:03:15** · You want to preserve the meaning of some population, but you-- I mean, you can't just change one thing.

**1:03:22** · The pop on chemistry, like the behavior may change dramatically.

**1:03:27** · So I'm just wondering whether it's just because-- how do you better preserve part of the-- how to render it hopeless, I say, it's not popular.

**1:03:38** · It might be.

**1:03:39** · I will let you actually go try to evaluate on GPQA and see if the chemistry segment-- if that hypothesis applies.

**1:03:47** · It is possible.

**1:03:51** · I mean, in every subject, when you go and from these models, the level of expertise varies for different reasons.

**1:03:58** · It's also possible the training data set was not that strong.

**1:04:02** · So it's out of distribution.

**1:04:05** · And the other comment that I was making earlier, if you-- basically, as you increase the number of documents-- This particular technique is able to leverage the fact that as you increase the number of documents, you can improve the performance just because you're not just making the context longer.

**1:04:22** · You're actually providing relevant context from each of those documents.

**1:04:29** · The other big thing that I want to highlight is that in multi-hop question answering, this is particularly relevant because in multi-hop question answering, you do tend to hit some amount of saturation in terms of performance with standard RAG.

**1:04:44** · And even with Agentic RAG, you do tend to hit some amount of saturation.

**1:04:49** · So in HotpotQA, in 2Wiki, MusiQue, or Bamboogle for example, if you just did RAG, for example, you would not hit the state-of-the-art numbers.

**1:04:59** · But with Search-o1, in a lot of these cases, you are hitting the highest numbers.

**1:05:05** · The bolded numbers across that particular line are coming from Search-o1 as a process.

**1:05:12** · So it is providing a lot of value, even in the multi-hop question answering across multiple documents.

**1:05:18** · Yes.

**1:05:18** · \[INAUDIBLE\] What are the precision and recall in the retrieval system?

**1:05:26** · That's a great question.

**1:05:28** · Why did the-- precision is the-- or the retrieval itself is above it, not the model.

**1:05:35** · So I think there is an assumption here that you did draw at least for the way I am explaining.

**1:05:40** · I mean, it's possible that you didn't retrieve the right documents, but if you look at the set of questions, I think the main claim that this paper is making is that if you find multiple relevant documents that are loosely correlated to what you're querying about, even then, once you put all of those documents in the context line, then that's-- you're asking the model to do a lot in terms of reasoning over that many documents.

**1:06:01** · So that's the claim that this particular paper is making.

**1:06:09** · So in terms of if you were to look at the takeaways here, the gains are definitely coming from the fact that it's able to reduce the uncertainty.

**1:06:18** · And the document quality or what you basically refine knowledge, both of those improve.

**1:06:26** · And in the multi-turn scenario, once you can figure out what you don't know it's able to-- even after refining across documents, it can do this iterative loop of improving upon that.

**1:06:40** · So it can construct better searches over multi-turn scenarios.

**1:06:43** · So in this particular case, the reasoning quality improves substantially because you're providing more relevant documents, and then you're also figuring out where the uncertainty is over multiple steps.

**1:06:55** · So effectively, you have the right documents.

**1:06:59** · And then you can correct yourself because when you put the documents in there, if you're still seeing uncertainty, then you have additional searches to go for.

**1:07:07** · So there were some numbers that the paper gives of the number of perhaps or wait or likely.

**1:07:13** · Basically, anything that quantifies uncertainty in the reasoning chains goes down substantially in this particular approach.

**1:07:19** · So they're basically analyzing the reasoning chains of the model.

**1:07:24** · So just to summarize what we covered here is that when we are building doing deep research agents on top of, say, the large reasoning models, that's a very effective way to bridge the knowledge gaps that exist in large language models.

**1:07:41** · But just doing simple retrieval augmented generation is often not enough.

**1:07:46** · And even with just fetching the documents, using tool calls is not enough.

**1:07:51** · You need to be able to do that effectively over multiple turns, and then identify the relevant information to refine which set of documents to keep.

**1:07:59** · So the large reasoning models by themselves often don't do a good job in scaling well if you put a lot of documents in there.

**1:08:08** · So this particular approach allows you to improve on that.

**1:08:12** · And larger models often do better.

**1:08:15** · And then-- OK, there's another paper that I wanted to cover, but I didn't end up covering.

**1:08:21** · So the Search-R1 stuff effectively varies from Search-o1 in that it teaches the model how to go search in an automatic way.

**1:08:29** · So what I wanted to say here was that Search-R1 versus Search-o1.

**1:08:34** · Search-o1 is closing the loop with a prompting-based approach.

**1:08:38** · Search-R1 can actually teach the model to do this with a reinforcement learning-based loop.

**1:08:45** · We will not cover this paper today because we are basically at the end, but it's worth going and taking a look at that paper.

**1:08:56** · Questions?

**1:08:58** · Yes.

**1:08:59** · I was just following this poster during the definition of a language model.

**1:09:03** · So when we generate an answer, are we supposed to have the ability to put a probability of that answer?

**1:09:13** · And I'm just wondering that when we have this, let's say 1,000 generations, each generation have a different probability, or at least in some extent.

**1:09:26** · And has there been some correlation between the right answers and the probabilities, or they are-- by definition, they are also a bit uncorrelated.

**1:09:37** · And also, same question to RAG, there's got to be-- I have a RAG augmented generation.

**1:09:49** · I can imagine that some of the-- maybe it messes up some of the definition.

**1:09:54** · Is there any difference in the probability of the answer?

**1:10:01** · I mean, that's a great experiment to go do.

**1:10:03** · So let me answer the first question.

**1:10:05** · And the second question, you will have to go experiment yourself.

**1:10:09** · So in the first question, typically-- so there's a lot of studies, but if you were to just take the output generation and compute the log probabilities of the output tokens and aggregate them in some meaningful way, not just sum them, you'll have to do some averaging or some geometric product or something.

**1:10:26** · What you'll find is that the models tend to be overconfident about what they-- overconfident, so if you were to calibrate that to the right answer, often you'll find that the correctness is-- Like if it's 50% correct, it will still be overconfident.

**1:10:44** · It'll be like 80% very confident that this is correct.

**1:10:47** · And this shows up in the ways in which if you try to correct the model outputs, it will sometimes be pretty strong in like, no, this is the right answer and will not change its mind.

**1:10:58** · So in some ways, the model outputs do tend-- have exhibited not high calibration and are more on the overconfident side.

**1:11:09** · And there have been research to try to get the model to estimate the confidence, say in a second pass or in a-- and try to do RL or RLHF on top of that to get the model to calibrate and do things so that it doesn't actually emit answers that it has low confidence over.

**1:11:29** · So there has definitely been efforts in that direction.

**1:11:33** · Different models exhibit different behaviors.

**1:11:35** · We don't know which lab did what.

**1:11:38** · So we just get these notions of oh, the model is hallucinating.

**1:11:43** · There is no correlation between the actual right answer both from the 1,000 and the-- I think there is a correlation in that if the answer is correct, then the model will likely get it correct.

**1:11:56** · But if the answer is incorrect, the model might be overconfident in feeling that it knows the answer.

**1:12:01** · That's been the observed pattern, but I think this is worth studying.

**1:12:07** · The hallucinations in just the ability of the model to know what they know is an active area of research.

**1:12:15** · And it's actually a great set of research projects if someone wants to pursue it.
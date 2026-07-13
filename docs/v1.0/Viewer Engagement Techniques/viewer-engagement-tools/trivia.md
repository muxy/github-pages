---
title: "Trivia Contests"
slug: "trivia"
excerpt: "For a more complex voting and reward system, Muxy provides a trivia service.  A trivia contest is made up of a series of multiple-choice questions."
hidden: true
metadata: 
  image: []
  robots: "index"
createdAt: "Wed Sep 15 2021 16:45:36 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Dec 15 2021 17:28:04 GMT+0000 (Coordinated Universal Time)"
---
The extension administrator acts as quiz-master, setting the questions and answer options, and designating which answer is considered correct.  During the event, individual questions can be set to an active of inactive state. For each active question, viewers can submit their answer choice.  They can change their choice as long as the question is active.

You can choose to present multiple questions in sequence or concurrently.  The extension administrator decides when to declare a winner, ending the event.

One common use of the trivia system is to pit broadcasters against each other. To make this easier, we provide optional team information in all trivia endpoints.   You can assign team points for correct choices, and the service updates an extension-wide leaderboard. The leaderboard displays a sum of correct answers from each viewer.

For example, we wrote an extension for the Video Game Awards that uses the trivia service. Each question specified a game category, and each of the candidate games in that category were answer options. Viewers would predict which game they thought would win. The show administrator would lock in the correct answer after it was announced, and reward teams with the most correct predictions.

> 🚧 This system is currently only available extension-wide, so all channels running an extension will see the same questions and be combined in the same leaderboard.
> 
> Currently trivia events are limited to 64 questions per extension. An extension cannot run multiple trivia events concurrently,

# Creating and Managing a Trivia Contest

The extension administrator (a user with the `broadcaster` or `admin` role) sets up the questions and answers, identifies the correct answer, and is responsible for any updates. Questions have an optional numerical `order` field for organizing question display and a `state` field that an administrator can set to show or hide a question and to enable or disable voting.

## Setting questions and options

To begin a Trivia contest event, an administrator-level account must create one or more questions with a set of associated options. 

Use these MEDKit methods to set up questions and options:

```javascript Setting and updating questions
// Create a question in the current contest
addExtensionTriviaQuestion(question_object);
// Change the options for an existing question
addExtensionTriviaOptionToQuestion(question_id, option_object);
```

- The _question_object_ is a JSON object that defines identifies a question and associates it with an answer option. It has these fields:



| Field | Value |
| --- | --- |
| id | A unique identifying string that associates this question with its answer options.  By convention, this is a lower-case, hyphen-separated alphanumeric string.  <br>  <br>If the question does not yet exist, it is created. If it already exists, new option information is added to it. |
| name | The descriptive string that identifies the question for the administrator. |
| short_name | A short display string for this question, suitable for a smaller display. |
| description | A longer display string for this question, suitable for a larger display. |
| image | Optional. A URL for an image to be displayed with the question. |
| order | Optional. The order of this question with respect to other questions in the contest.  The use of ordering is developer-defined. |




Each call that uses a given question ID associates an option with that question. The following example creates a single question, named "first-question", with three answer options.

```javascript Admin sets a question with two options
const opts = new Muxy.DebuggingOptions();
opts.role('admin');
Muxy.debug(opts);

const medkit= new Muxy.SDK();
medkit.addExtensionTriviaQuestion({
  id: 'first-question',
  name: 'This is the 1st trivia question',
  short_name: '1st Question',
  description: 'This is the first question viewers will be able to vote on',
  image: 'https://picsum.photos/200/200/?random',
  order: 1
});

medkit.addExtensionTriviaOptionToQuestion('first-question', {
  id: 'first-option',
  name: "The first question's first option",
  short_name: '1st option',
  description: 'This is the first option of the first question',
  image: 'https://picsum.photos/200/200/?random',
  order: 1
});

medkit.addExtensionTriviaOptionToQuestion('first-question', {
  id: 'second-option',
  name: "The first question's second option",
  short_name: '2nd option',
  description: 'This is the second option of the first question',
  image: 'https://picsum.photos/200/200/?random',
  order: 1
});

medkit.addExtensionTriviaOptionToQuestion('first-question', {
  id: 'third-option',
  name: "The first question's third option",
  short_name: '3rd option',
  description: 'This is the third option of the first question',
  image: 'https://picsum.photos/200/200/?random',
  order: 1
});
```

## Displaying questions

It is entirely up to the developer how you display your trivia questions to viewers. The `name` value is intended to identify the question for the admin who runs the event. The text provided by the `short_name` and `description` fields gives you an opportunity to tailor the UI according to screen size. 

In our Video Games Awards extension, for example, we displayed an image together with the `short_name` or `description` value,  depending on what screen the viewer was on. 



![1024](https://files.readme.io/3af5e52-game_awards.png)




The viewer's extension must also display answer options for each question, and allow the viewer to submit their choice of answer.

## Updating questions and options

To change a question or option's values, call the `add` methods with the `id` of an existing question or option. Any new value replaces the existing one.

```javascript Amin updates question text
const opts = new Muxy.DebuggingOptions();
opts.role('admin');
Muxy.debug(opts);

const medkit= new Muxy.SDK();
medkit.addExtensionTriviaQuestion({
  id: 'first-question',
  name: 'This is the 1st trivia question',
  short_name: '1st Question',
  description: 'This is the first question viewers will be able to vote on',
  image: 'https://picsum.photos/200/200/?random',
  order: 1
});

medkit.addExtensionTriviaQuestion({
  id: 'first-question',
  name: 'This is the 1st trivia question with correct text',
  short_name: '1st Question Corrected',
  description: 'This is the first question viewers will be able to vote on',
  image: 'https://picsum.photos/300/300/?random',
  order: 1
});
```

To remove a question or option, use the `remove` methods:

```javascript Admin removes a question
// remove an option
medkit.removeExtensionTriviaOptionFromQuestion('first-question', 'first-option');
// remove a question
medkit.removeExtensionTriviaOptionFromQuestion('first-question');
```

## Setting or updating question state

Every trivia question has a `state` field that the administrator can use to restrict or allow viewer access to trivia questions.  

To set the state, use the `setExtensionTriviaQuestionState()` method:

```javascript Setting questions
medkit.setExtensionTriviaQuestionState(question_id, state, winning_option_id);
```

- _question_id_ identifies the question whose state is being set.
- _state_ is the new state value. A `Muxy.TriviaQuestionState` constant. 
- _winning_option_id_ is optional. Provide this when transitioning to the `Results` state, to identify the winning option. The server uses this information to calculate the vote result percentages and update the leaderboard.

The following state constants are defined:

| State constant | Effect                                                                                                                                                 |
| :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Inactive`     | This question is not returned to requests from viewers or broadcasters.                                                                                |
| `Unlocked`     | This question is returned to and accepts votes from viewers.                                                                                           |
| `Locked`       | This question is returned to request from viewers, but the service does not  accepts votes.                                                            |
| `Results`      | This question is returned to request from viewers,  and includes vote result values in the response. The service does not accept any additional votes. |

The following example sets a question to the "Unlocked" state, allowing viewers to retrieve it and submit votes. 

```javascript Admin sets a question
const opts = new Muxy.DebuggingOptions();
opts.role('admin');
Muxy.debug(opts);

const medkit= new Muxy.SDK();
medkit.setExtensionTriviaQuestionState('first-question', Muxy.TriviaQuestionState.Unlocked);
```

When transitioning to `Results` state, you must provide the option ID of the winning option, as in the following example. 

```javascript Admin declares winning option
const opts = new Muxy.DebuggingOptions();
opts.role('admin');
Muxy.debug(opts);

const medkit= new Muxy.SDK();
medkit.setExtensionTriviaQuestionState('first-question', Muxy.TriviaQuestionState.Results, 'first-option');
```

# Examining Contest Status

Any user can request the list of current questions at any time. The response varies according to the caller's access rights and the question status. 

- Viewers do not see trivia questions that are listed as `inactive`, but admins do. 
- The `results` field of each question contains vote information for the current user, and winner information if a winner has been chosen by the administrator.

In the following example, a viewer requests questions for the current event, using the `SDK.getExtensionTriviaQuestions()` method, and prints the response.

```javascript Retrieve question in Viewer extension
const opts = new Muxy.DebuggingOptions();
opts.role('viewer');
Muxy.debug(opts);

const medkit= new Muxy.SDK();
medkit.getExtensionTriviaQuestions().then(response => {
  console.log(`Found ${response.questions.length} questions`);
  response.questions.forEach(q => {
    console.log(q.name);
    q.options.forEach(o => {
      let optionStr = `\t- ${o.name}`;
      if (q.results) {
        // If the current viewer sent a prediction for this
        // question, it will come back in the `you` field of
        // the `results` object. This field will be `undefined`
        // if no prediction was sent.
        if (q.results.you && q.results.you === o.id) {
          optionStr += ' (your vote)';
        }

        // If an admin has set a winning option, the id of the
        // winning option will be returned in the `winner` field.
        if (q.results.winner && q.results.winner === o.id) {
          optionStr += ' !winner!';
        }
      }

      console.log(optionStr);
    });
  });
});
```

For the examples above, this script might output:

```
This is the 1st trivia question
  - The first question's first option (your vote)
  - The first question's second option !winner!
  - The first question's third option
```

# Choosing Options

Any user can choose an option for a given question as long as voting for that question is open.  Use the `setExtensionTriviaQuestionVote()` method to send a user's vote to the server.

```javascript Send viewer vote
const opts = new Muxy.DebuggingOptions();
opts.role('viewer');
Muxy.debug(opts);

const medkit = new Muxy.SDK();
// Current user is voting for the second option of the first question.
medkit.setExtensionTriviaQuestionVote('first-question', 'second-option');
```

Votes are unique per user; that is, a given question retains only one vote value for a given user. If a user sends additional votes giving the same question ID,  that user's vote changes  to the latest value.

# Trivia Teams and Leaderboard

> ❗️ Under construction
> 
> - _Is leaderboard ONLY used with teams?_ 
> - _Is "prediction" the only kind of response expected? or is that just the example case?_
> - _Is this feature available through JS, or just REST API?_

A viewer is assigned to a team the first time they successfully submit a prediction.  The team is set to the channel they are viewing when the prediction is sent. After this point, they can submit votes from any channel, but their predictions (and any associated leaderboard points) will count towards their original team. It is not possible for a viewer to change their team.

Broadcasters always cast votes for their own channel and are returned in results as the special `broadcaster_correct` field.

In the past _((is this true now?))_ we have gated this feature, by showing a dialog to the viewer when they submit their first vote and confirming that they want to join the team of the current channel they are watching.

## Leaderboard values

Leaderboard values are updated only when a winner is declared for a new question, but an admin can request the current status of a prediction leaderboard at any time. 

Make this request with a call to `sdk.getExtensionTriviaLeaderboard()`, as in the following example.

```javascript Request leaderboard status
const opts = new Muxy.DebuggingOptions();
opts.role('admin');
Muxy.debug(opts);

const medkit = new Muxy.SDK();
medkit.getExtensionTriviaQuestions().then({ questions } => {
  medkit.getExtensionTriviaLeaderboard().then({ leaderboard } => {
    console.log('Current Leaderboard');
    console.log('-------------------');

    leaderboard.forEach(team => {
      console.log(`\nTeam's Twitch ID: ${team.team_id}`);
      console.log(`Current Score: ${team.combined_score}`);
      team.questions.forEach(results => {
        console.log('* ' + questions.find(q => q.id === results.question_id).short_name);
        console.log(`\t - Broadcaster was ${results.broadcaster_correct ? 'correct' : 'incorrect'}`);
        console.log(`\t - Team had ${Math.floor(results.team_participation * 100)}% participation`);
        console.log(`\t - And were ${Math.floor(results.percent_correct * 100)}$ correct`);
        console.log(`\t = There were ${results.team_votes} total votes`);
      });
    });
  });
});
```

When the response is received, this call prints the results:

```text Console output
Current Leaderboard
-------------------

Team's Twitch ID: 123456
Current Score: 100000
* This is the 1st trivia question
  - Broadcaster was correct
  - Team had 83% participation
  - And were 68% correct
  - There were 372 total votes

Team's Twitch ID: 654321
Current Score: 82983
* This is the 1st trivia question
  - Broadcaster was incorrect
  - Team had 49% participation
  - And were 38% correct
  - There were 2760 total votes
```

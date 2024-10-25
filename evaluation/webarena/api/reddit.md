## Forums

### List All Forums

To retrieve the names of all the forums, you could use the API `get http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/forums/all`.

#### Response

The response contains HTML contents including the names of all the forums sorted by alphabetical order. For example,
```html
<li><a href="/f/allentown">allentown</a></li>
```
this means a forum named `allentown`, and to retrieve the contents in this forum, you would need to do `get http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/f/allentown`.


### **Get Forum by ID**
To retrieve a forum by its ID, use the `get_forum_by_id` function.  
To use this function, run:

```python
from utils import get_forum_by_id
```

#### **Input Parameters**:
- **forum_id** (int): The ID of the forum.

#### **Response**:
- Returns a JSON object containing the forum details.

---

### **Create a New Forum**
To create a new forum, use the `create_forum` function.  
To use this function, run:

```python
from utils import create_forum
```

#### **Input Parameters**:
- **forum_name** (str): The name of the new forum.
- **title** (str): The title of the new forum.
- **sidebar** (str): The sidebar content for the forum.
- **description** (str): The description of the forum.

#### **Response**:
- Returns a JSON object containing the result of the forum creation.

---

### **Update a Forum**
To update an existing forum, use the `update_forum` function.  
To use this function, run:

```python
from utils import update_forum
```

#### **Input Parameters**:
- **forum_id** (int): The ID of the forum to be updated.
- **forum_name** (str): The new name of the forum.
- **title** (str): The new title of the forum.
- **sidebar** (str): The updated sidebar content.
- **description** (str): The updated description.

#### **Response**:
- Returns a JSON object containing the result of the forum update.

### **Subscribe and Unsubscribe**

#### Subscribe to a Forum
To subscribe to a forum, use the predefined `utils` function `subscribe_forum`.  
To use this function, run:

```python
from utils import subscribe_forum
```

#### **Input Parameters**:
- **forum_name** (str): The name of the forum you want to subscribe to. Example: `'relationship_advice'`.

#### **Response**:
- Returns a JSON object containing the result of the subscription.

---

#### Unsubscribe from a Forum
To unsubscribe from a forum, use the predefined `utils` function `unsubscribe_forum`.  
To use this function, run:

```python
from utils import unsubscribe_forum
```

#### **Input Parameters**:
- **forum_name** (str): The name of the forum you want to unsubscribe from. Example: `'relationship_advice'`.

#### **Response**:
- Returns a JSON object containing the result of the unsubscription.

### Retrieve All Submissions to a Forum

To retrieve all submissions to a forum, you could use the API `get http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/f/{forum_name}`. For example, `get http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/f/allentown`

#### Sort Submissions

You could sort the submissions by `hot`, `new`, `active`, `top`, `controversial`, and `most_commented`.

For `hot`, `new`, and `active`, you could sort by these attributes using the API format `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/f/{forum_name}/{attribute}`. For example, `get http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/f/allentown/hot`.

For `top`, `controversial`, and `most_commented`, you could sort by these attributes using the API format `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/f/{forum_name}/{attribute}?t={time}`. For $time, you could choose from `day` (which means the past 24 hours), `week` (which means the past 7 days), `month` (which means the past month), `year` (which means the past yeaer), and `all` (which means all times). For example, `get http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/f/allentown/most_commented?t=day` will get you the submissions in the past 24 hours, sorted by number of comments; `get http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/f/allentown/most_commented?t=all` will get you all submissions until now, sorted by number of comments.

#### Retrieve a Specific Submission and All Comments to It

If you already has the submission_id that you would like to retrieve, then you are good to use the API `get http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/{submission_id}`. For example, the submission_id for the submission with title 'New area code?' to the forum 'allentown' has the submission_id `123256`, then you could do `get http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/123256` to retrieve the submission and all comments to this submission.

However, if you don't have the submission_id to the submission you would like to retrieve, but you have a keyword or the title of the submission and the name of the forum, then you could first call `get http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/f/{forum_name}`, and then search for the keyword of the submission in the html response, and the locate the line with format `href="/f/{forum_name}/{submission_id}/...`. For example, if you would like to retrieve the submission to `allentown` with keyword `area`, then you could first call `get http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/f/allentown`, and then search for `area`. For instance, the response contains the following lines:

```html
<div class="submission__row">

      <div class="submission__inner">
        <header class="submission__header">
          <div class="submission__title-row break-text"><h1 class="submission__title unheaderize inline"><a href="/f/allentown/123256/new-area-code"
         class="submission__link"
                  rel=""
          target="_self"
        >New area code?</a></h1>


                      </div>

          <p class="submission__info">
            <span class="text-sm fg-muted">
              Submitted by         <a href="/user/Francis-pencovic" class="submission__submitter fg-inherit"><strong>Francis-pencovic</strong></a>    <small class="fg-grey text-sm user-flag">t3_11xxi00</small>
   <time class="submission__timestamp"
        data-controller="relative-time"
        datetime="2023-03-21T22:40:42+00:00"
        title="March 21, 2023 at 10:40:42 PM UTC">on March 21, 2023 at 10:40 PM</time>
```
then, `123256` is the submission_id you want. You could find this submission_id by locating the line `href="/f/allentown/123256/new-area-code"`. Then you could call `get http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/123256` to retrieve the submission and all comments to this submission.

### Retrieve All Comments to a Forum

To retrieve all comments to a forum, you could use the API `get http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/f/{forum_name}/comments`. For example, `get http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/f/allentown/comments`.

## User

### **Update User Bio**
To update the biography of the current user, use the `update_bio` function.  
To use this function, run:

```python
from utils import update_bio
```

#### **Input Parameters**:
- **bio** (str): The new biography content.

#### **Response**:
- Returns a dictionary indicating whether the update was successful (`{"updated": True}`) or not (`{"updated": False}`).

### Other Functionalities
To retrieve the information of a user, you could use the API `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/user/{username}`.

To retrieve the submissions of a user, you could use the API `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/user/{username}/submissions`.

To retrieve the comments of a user, you could use the API `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/user/{username}/comments`.

To retrieve the preferences of a user, you could use the API `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/user/{username}/preferences`.


Here's the API documentation for the functions you provided in `utils.py`. This documentation is organized by different functionalities such as subscribing to forums, voting on submissions and comments, etc.


## Submissions

### **Get a Submission by Submission ID**
To get a submission by its ID, use the `get_submission_by_id` function.  
To use this function, run:

```python
from utils import get_submission_by_id
```

#### **Input Parameters**:
- **submission_id** (int): The ID of the submission.

#### **Response**:
- Returns an json containing the submission information.

### **Get Votes for a Submission**
To get the number of votes for a submission, use the `get_submission_votes` function.  
To use this function, run:

```python
from utils import get_submission_votes
```

#### **Input Parameters**:
- **submission_id** (int): The ID of the submission to check the votes for.

#### **Response**:
- Returns an integer representing the net votes for the submission.

---

### **Upvote a Submission**
To upvote a submission, use the `upvote_submission` function.  
To use this function, run:

```python
from utils import upvote_submission
```

#### **Input Parameters**:
- **submission_id** (int): The ID of the submission to upvote.

#### **Response**:
- Returns a JSON object containing the result of the upvote.

---

### **Downvote a Submission**
To downvote a submission, use the `downvote_submission` function.  
To use this function, run:

```python
from utils import downvote_submission
```

#### **Input Parameters**:
- **submission_id** (int): The ID of the submission to downvote.

#### **Response**:
- Returns a JSON object containing the result of the downvote.

---

### **Remove Vote from a Submission**
To unvote a submission, use the `unvote_submission` function.  
To use this function, run:

```python
from utils import unvote_submission
```

#### **Input Parameters**:
- **submission_id** (int): The ID of the submission to unvote.

#### **Response**:
- Returns a JSON object containing the result of the unvote.

---

## Comments

### **Get All Comments**
To retrieve all comments from a submission, use the `get_all_comments` function.  
To use this function, run:

```python
from utils import get_all_comments
```

#### **Response**:
- Returns a JSON object containing a list of all comments.

---

### **Get Comment by ID**
To retrieve a specific comment by its ID, use the `get_comment_by_id` function.  
To use this function, run:

```python
from utils import get_comment_by_id
```

#### **Input Parameters**:
- **comment_id** (int): The ID of the comment.

#### **Response**:
- Returns a JSON object containing the comment data.

---

### **Update Comment by ID**
To update the content of a comment, use the `update_comment_by_id` function.  
To use this function, run:

```python
from utils import update_comment_by_id
```

#### **Input Parameters**:
- **comment_id** (int): The ID of the comment to be updated.
- **new_comment_content** (str): The new content for the comment.

#### **Response**:
- Returns the updated comment as text.

---


### **Get Votes for a Comment**
To get the number of votes for a comment, use the `get_comment_votes` function.  
To use this function, run:

```python
from utils import get_comment_votes
```

#### **Input Parameters**:
- **submission_id** (int): The ID of the submission where the comment is posted.
- **comment_id** (int): The ID of the comment to check the votes for.

#### **Response**:
- Returns an integer representing the net votes for the comment.

---

### **Upvote a Comment**
To upvote a comment, use the `upvote_comment` function.  
To use this function, run:

```python
from utils import upvote_comment
```

#### **Input Parameters**:
- **submission_id** (int): The ID of the submission where the comment is posted.
- **comment_id** (int): The ID of the comment to upvote.

#### **Response**:
- Returns a JSON object containing the result of the upvote.

---

### **Downvote a Comment**
To downvote a comment, use the `downvote_comment` function.  
To use this function, run:

```python
from utils import downvote_comment
```

#### **Input Parameters**:
- **submission_id** (int): The ID of the submission where the comment is posted.
- **comment_id** (int): The ID of the comment to downvote.

#### **Response**:
- Returns a JSON object containing the result of the downvote.

---

### **Remove Vote from a Comment**
To unvote a comment, use the `unvote_comment` function.  
To use this function, run:

```python
from utils import unvote_comment
```

#### **Input Parameters**:
- **submission_id** (int): The ID of the submission where the comment is posted.
- **comment_id** (int): The ID of the comment to unvote.

#### **Response**:
- Returns a JSON object containing the result of the unvote.

---

## **Commenting on Submissions**

### **Post a Comment on a Submission**
To post a new comment on a submission, use the `post_comment` function.  
To use this function, run:

```python
from utils import post_comment
```

#### **Input Parameters**:
- **submission_id** (int): The ID of the submission where the comment will be posted.
- **comment** (str): The content of the comment.

#### **Response**:
- Returns the URL of the posted comment.

---

### **Reply to a Comment**
To reply to an existing comment, use the `reply_comment` function.  
To use this function, run:

```python
from utils import reply_comment
```

#### **Input Parameters**:
- **submission_id** (int): The ID of the submission where the comment is posted.
- **comment_id** (int): The ID of the comment to reply to.
- **comment** (str): The reply content.

#### **Response**:
- Returns the URL of the posted reply.

---

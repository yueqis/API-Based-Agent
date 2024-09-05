## Forums

### List All Forums

To retrieve the names of all the forums, you could use the API `get http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/forums/all`.

#### Response

The response contains HTML contents including the names of all the forums sorted by alphabetical order. For example,
```html
<li><a href="/f/allentown">allentown</a></li>
```
this means a forum named `allentown`, and to retrieve the contents in this forum, you would need to do `get http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/f/allentown`.

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

To retrieve the information of a user, you could use the API `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/user/{username}`.

To retrieve the submissions of a user, you could use the API `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/user/{username}/submissions`.

To retrieve the comments of a user, you could use the API `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/user/{username}/comments`.

To retrieve the preferences of a user, you could use the API `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/user/{username}/preferences`.

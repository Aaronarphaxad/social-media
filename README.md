# Social Media App

Live Demo: https://socialnetwork44.herokuapp.com/

Youtube preview link: https://youtu.be/RpwAE6cMOXI

### Brief Description

This is a Twitter-like, full-stack social media app built with Django and javascript. Styled with CSS and bootstrap CDN. The aim of building this project was to learn how to build fetch APIs at the back-end. I learnt a lot building this project, and sharpen my skills on things like Django model manager, javascript AJAX, system architecture, Django pagination, and how to write tests for your app.

#### Features

- Login, Log out and user authentication system
- New post: logged in users can make posts that would be visible by everyone with access to the link, but only registered users can like their post. Empty posts cannot be sent.
- All posts: This page contains every post ever posted on the app. Users who aren't signed in or registered can view posts.
- Profile page: The profile page displays all the user information including number of followers and people the user follows(following). When a username is clicked on, it takes you to the profile page of that user and shows the follow(or following) and unfollow button. All the buttons and features are functional.
- Following: This page contains the posts of everyone the user follows.
- Pagination: Posts in the profile and following pages are divided into specific pages and displayed in pagegs which allows you to navigate the posts without leaving the page.
- Edit post: Users can edit a post they've posted in the past, others users cannot. This feature was implemented using a bootstrap modal. The new edited post cannot be blank and you cannot send an unedited post.
Like and Unlike: Signed in users can like and unlike posts. Posts can only be liked once.
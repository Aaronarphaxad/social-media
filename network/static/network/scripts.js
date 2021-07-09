document.addEventListener('DOMContentLoaded', function() {
    // document.querySelector('#following').addEventListener('click', )
    // document.querySelector('#profile_view').addEventListener('click', loadProfile)
});

document.querySelector('#allPosts').addEventListener('click', load_page());


let composeForm = document.querySelector('#compose-form');
composeForm.addEventListener('submit', () => {
    let post = document.getElementById('post-data').value;
    if (post == "") {
        alert("Can't send an empty post, be creative ;)")
    } else {
        // Send Post request to the API to send posts
        fetch('/network', {
                method: 'POST',
                body: JSON.stringify({
                    post: post
                })
            }).then(response => response.json())
            .then(result => {
                if (result.error) {
                    console.log(`error sending post ${result.error}`)
                } else {
                    load_page()
                }
            })
    }
})



// Function to load page
function load_page() {
    // Send get request to get posts
    fetch("/network/posts")
        .then(response => response.json())
        .then(posts => {
            let view = document.getElementById('post_view');
            // view.innerHTML = ""
            let allPosts = posts["data"]
            let loggedInUser = posts["loggedInUser"]
            for (let eachpost of allPosts) {
                // create post element
                let div = createElement('div', {
                    'id': 'post_card',
                    'class': "card m-3 p-3 shadow",
                    'style': "background-color: #fefdd1"
                });
                // get post details
                let { time, post, username, userId, likes, postId } = eachpost

                let date = time.slice(0, 10)
                let newtime = time.slice(11, 16)
                let editButtonClass = username === loggedInUser ? "edit" : ""



                // construct the post card
                div.innerHTML = `<div class="d-flex justify-content-between"><a style="text-decoration: none;" href="network/profile/${userId}">@${username}</a> <span style="background-color: #fefdd1;" data-id="${postId}" data-post="${post}" class="material-icons editButton" type="button" data-toggle="modal" data-target="#exampleModal">
                ${editButtonClass}
                </span>
                </div> 
                <div class="mt-3 mr-3 mb-3"><span id="post-${postId}">${post}</span></div>
                <div class="d-flex">
                ${newtime} . 
                ${date}
            </div><hr>
            <div class="d-flex mt-2"><span class="mr-2">${likes}</span>  <a class="likeButtons" href="" ><i id=${postId} class="material-icons mr-2 buttonss">thumb_up</i></a> <a href="#" class="dislikeButtons"><i id=${postId} class="material-icons mr-2 buttonss">thumb_down</i></a><div>
            
            `
                    // append each post to view container
                view.append(div)

                console.log(loggedInUser)
                if (loggedInUser == 'AnonymousUser') {
                    let editButton = document.querySelectorAll('.editButton')
                    editButton.forEach(button => {
                        button.style.display = "none";
                    })

                    document.getElementById('compose_view').style.display = "none";

                }


            }
            // End of posts loop

            //         let paginator = createElement('div');

            //         paginator.innerHTML = `

            //         <nav aria-label="Page navigation example">
            //   <ul class="pagination justify-content-center">
            //     {% if ${allPosts}.has_previous %}
            //       <li class="page-item">
            //         <a class="page-link" href="?page= ${allPosts}.previous_page_number">Previous</a>
            //       </li>
            //     {% else %}
            //       <li class="page-item disabled">
            //         <a class="page-link" href="#" tabindex="-1" aria-disabled="true">Previous</a>
            //       </li>
            //     {% endif %}
            //     {% for i in ${allPosts}.paginator.page_range %}
            //       {% if ${allPosts}.number == i %}
            //         <li class="page-item active" aria-current="page">
            //           <span class="page-link">
            //             {{ i }}
            //             <span class="sr-only">(current)</span>
            //           </span>
            //         </li>
            //       {% else %}
            //         <li class="page-item"><a class="page-link" href="?page={{ i }}">{{ i }}</a></li>
            //       {% endif %}
            //     {% endfor %}
            //     {% if ${allPosts}.has_next %}
            //       <li class="page-item">
            //         <a class="page-link" href="?page={{ ${allPosts}.next_page_number }}">Next</a>
            //       </li>
            //     {% else %}
            //       <li class="page-item disabled">
            //         <a class="page-link" href="#" tabindex="-1" aria-disabled="true">Next</a>
            //       </li>
            //     {% endif %}
            //   </ul>
            // </nav>


            //         `

            // get csrf token to send for security
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            // get like/dislike buttons
            let likeButton = document.querySelectorAll('.likeButtons');
            let dislikeButton = document.querySelectorAll('.dislikeButtons');
            // add eventlistener for like buttons
            likeButton.forEach((button) => {
                    button.addEventListener('click', function(e) {
                        e.preventDefault()
                            // send put request when like button clicked
                        const post_id = e.target.id
                        fetch(`/network/like/${post_id}`, {
                                headers: { 'X-CSRFToken': csrftoken },
                                method: "PUT",
                                body: JSON.stringify({ likes: true })
                            })
                            .then(response => {
                                location.reload();
                                console.log("Like updated")
                            })
                    })
                })
                // end of like event listener

            // add eventlistener for dislike buttons
            dislikeButton.forEach((button) => {
                    button.addEventListener('click', function(e) {
                        e.preventDefault()
                        const post_id = e.target.id
                        fetch(`/network/dislike/${post_id}`, {
                                headers: { 'X-CSRFToken': csrftoken },
                                method: "PUT",
                                body: JSON.stringify({ likes: false })
                            })
                            .then(response => {
                                location.reload();
                                console.log("disliike updated")
                            })
                    })
                })
                // end of dislike event listener


            document.getElementById('profile').addEventListener('click', function() {

                let followButton = document.querySelector('#followButton');
                let unfollowButton = document.querySelector('#unfollowButton');
                if (followButton) {
                    followButton.addEventListener('click', function(event) {
                        event.preventDefault();
                        fetch(`/network/profile/follow/${user}`, {
                                method: "POST",
                                body: JSON.stringify({ follower: user })
                            }).then(response => response.json())
                            .then(result => {
                                if (result.error) {
                                    console.log(`Error sending follow request: ${result.error}`)
                                    return
                                } else {
                                    document.getElementById('followButton').innerHTML = "Following";
                                }

                            })
                    })

                }
                // end of follow event listene
            })

        })
        // End of post GET request




}
// End of load page function







// Function to create element
function createElement(element, attribute, inner) {
    if (typeof(element) === "undefined") {
        return false;
    }
    if (typeof(inner) === "undefined") {
        inner = "";
    }
    var el = document.createElement(element);
    if (typeof(attribute) === 'object') {
        for (var key in attribute) {
            el.setAttribute(key, attribute[key]);
        }
    }
    if (!Array.isArray(inner)) {
        inner = [inner];
    }
    for (var k = 0; k < inner.length; k++) {
        if (inner[k].tagName) {
            el.appendChild(inner[k]);
        } else {
            el.appendChild(document.createTextNode(inner[k]));
        }
    }
    return el;
}


// Create post and id variables to send 
let id;
let prevPost;

// Bootstrap jquery for modal
$('#exampleModal').on('show.bs.modal', function(event) {
    let button = $(event.relatedTarget) // Button that triggered the modal
        // get the post and id from the button
    prevPost = button.data('post');
    id = button.data("id")
    let modal = $(this)
        // populate the textarea with the post to edit
    modal.find('.modal-body textarea').val(prevPost)
});

// Event listener for send button on edit post modal
let sendButton = document.getElementById("sendEdit");
sendButton.addEventListener("click", (e) => {
    let newPost = document.querySelector(".modal-body textarea").value
        // If post is not empty or unchanged, send PUT request to the route
    if (!((newPost === "") || (newPost === prevPost))) {
        let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch(`network/edit/${id}`, {
                headers: { 'X-CSRFToken': csrftoken },
                method: "PUT",
                body: JSON.stringify({ post: newPost })
            })
            .then(result => {
                if (result.error) {
                    console.log(`error sending post ${result.error}`)
                } else {
                    alert("Post updated :)")
                    location.reload();
                    console.log("Post updated")
                }
            });

    } else {
        alert("No changes made or empty post!")
    }

})
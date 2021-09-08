import React, { Component } from "react";
import "./Feed.css";
import InfiniteScroll from "react-infinite-scroll-component";
import Navbar from "../../components/Navbar/Navbar";
import Post from "../Post/Post";

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export default class Feed extends Component {
  constructor() {
    super();
    this.state = {
      requestUserData: {},
      totalPosts: 0,
      currentPost: 0,
      userSuggestions: {},
      page: 0,
      posts: [],
      hasMore: true,
    };
    this.getUserSuggestions();
    this.getPosts();
  }
  
  setUserData = (data) => {
    this.setState({ requestUserData: data });
  };

  getUserSuggestions = async () => {
    await fetch("/api/getUserSuggestions/", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        Accept: "application/json",
        "X-Requested-With": "XMLHttpRequest", //Necessary to work with request.is_ajax()
        "X-CSRFToken": getCookie("csrftoken"),
      },
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        this.setState({ userSuggestions: data.response });
      });
  };

  

  getPosts = async () => {
    await fetch("/", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        Accept: "application/json",
        "X-Requested-With": "XMLHttpRequest", //Necessary to work with request.is_ajax()
        "X-CSRFToken": getCookie("csrftoken"),
      },
      credentials: "include",
      body: JSON.stringify({ page: this.state.page }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.stop) {
          this.setState(
            {
              posts: [...this.state.posts, ...Object.values(data.response)],
              hasMore: data.hasMore,
            },
            
          );
        } else {
          this.setState(
            {
              posts: [...this.state.posts, ...Object.values(data.response)],
              hasMore: data.has_more,
              page: this.state.page + 1,
            },
            
          );
        }
      });
  };

  render() {
    return (
      <>
        <Navbar setUserData={this.setUserData} />
        <div className="content">
          <div className="main-content">
            <InfiniteScroll
              dataLength={this.state.posts.length}
              next={this.getPosts}
              hasMore={this.state.hasMore}
              loader={<h4>Loading...</h4>}
              endMessage={
                <p style={{ textAlign: "center" }}>
                  <b>Yay! You have seen it all</b>
                </p>
              }
              height={800}
              refreshFunction={() => {
                console.log("refreshed");
              }}
              pullDownToRefresh
              pullDownToRefreshThreshold={50}
              pullDownToRefreshContent={
                <h3 style={{ textAlign: "center" }}>
                  &#8595; Pull down to refresh
                </h3>
              }
              releaseToRefreshContent={
                <h3 style={{ textAlign: "center" }}>
                  &#8593; Release to refresh
                </h3>
              }
            >
              
                {this.state.posts.map(post => (
                  <Post post={post} key={post.custom_id} requestUser={this.state.requestUserData}/>
    ))}
              
            </InfiniteScroll>
          </div>
          <div className="suggestions">
            <div className="personalinfo row mt-4">
              <div className="col-4 flex-v-center">
                <a href={"/" + this.state.requestUserData.username}>
                  <img
                    className="main-dp sugg-user-icon"
                    src={this.state.requestUserData.dp_url}
                    alt="Your Profile Pic"
                  />
                </a>
              </div>
              <div className="col-5 flex-h-center">
                <div
                  className="row "
                  style={{ fontSize: "19px", textAlign: "center" }}
                >
                  <a
                    href={"/" + this.state.requestUserData.username}
                    className="link"
                  >
                    <b>{this.state.requestUserData.username}</b>
                  </a>
                </div>
                <div className="row " style={{ fontSize: "13px" }}>
                  {this.state.requestUserData.name}
                </div>
              </div>
            </div>
            <div className="sugg mt-3">
              <div className="row">
                <div
                  className="col-8"
                  style={{
                    textAlign: "left",
                    fontWeight: 600,
                    color: "rgb(133, 133, 133)",
                  }}
                >
                  Suggestions for you
                </div>
                <div
                  className="col-4 flex-v-center"
                  style={{ fontSize: "13px" }}
                >
                  <a href="/explore/suggested/" className="normalize-link">
                    <b>See All</b>
                  </a>
                </div>
              </div>
              <div className="main-sugg mt-4">
                {Object.keys(this.state.userSuggestions).length === 0
                  ? "No Suggestions"
                  : Object.keys(this.state.userSuggestions).map((item) => (
                      <div
                        className="sugg-item row mt-2"
                        key={this.state.userSuggestions[item].username}
                      >
                        <div className="col-3">
                          <a
                            href={
                              "/" + this.state.userSuggestions[item].username
                            }
                          >
                            <img
                              className="sugg-icon"
                              src={this.state.userSuggestions[item].dp_url}
                              alt=""
                            />
                          </a>
                        </div>
                        <div className="col-9 sugg-username">
                          <a
                            className="link"
                            href={
                              "/" + this.state.userSuggestions[item].username
                            }
                          >
                            <b>{this.state.userSuggestions[item].username}</b>
                          </a>
                        </div>
                      </div>
                    ))}
              </div>
            </div>
          </div>
        </div>
      </>
    );
  }
}

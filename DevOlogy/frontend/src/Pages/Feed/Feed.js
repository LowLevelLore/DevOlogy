import React, { Component } from "react";
import "./Feed.css";
import InfiniteScroll from "react-infinite-scroll-component";
import Navbar from "../../components/Navbar/Navbar";

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
    };
    this.getRequestUserInfo();
  }
  getRequestUserInfo = async () => {
    await fetch("/api/getRequestUserInfo/", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        Accept: "application/json",
        "X-Requested-With": "XMLHttpRequest", //Necessary to work with request.is_ajax()
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        this.setState({ requestUserData: data.response });
      });
  };
  render() {
    return (
      <>
        <Navbar userData={this.state.requestUserData}/>
        <div className="main" id="main">
          <div className="cont infinite-container" id="ic"></div>
        </div>

        <div className="suggestions">
          <div className="container-fluid">
            <div className="personalinfo row mt-4">
              <div className="col-4 flex-v-center">
                <a href={this.state.requestUserData.username}>
                  <img
                    className="main-dp"
                    alt="Your Profile Pic"
                    src={this.state.requestUserData.dp_url}
                  />
                </a>
              </div>
              <div className="col-5">
                <div
                  className="row ct  flex-h-center"
                  style={{ fontSize: "17px" }}
                >
                  <a href="" className="normalize-link">
                    <b>{this.state.requestUserData.username}</b>
                  </a>
                </div>
                <div className="row ct  flex-h-center">
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
                    fontWeight: "600",
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
              <div className="main-sugg mt-3">
                <b>No Suggestions</b>

                <div className="row mt-2">
                  <div className="col-3 flex-v-center">
                    <a href="">
                      <img className="sugg-dp" src="" />
                    </a>
                  </div>
                  <div className="col-6">
                    <div className="sp-row">
                      <a
                        className="normalize-link"
                        href=""
                        style={{ fontSize: "15px" }}
                      >
                        <b></b>
                      </a>
                    </div>
                    <div className="sp-row"></div>
                  </div>
                  <div
                    className="col-3 flex-v-center"
                    style={{ textAlign: "center", fontSize: "13px" }}
                  >
                    <a className="blue normalize-link sugg-follow" id="">
                      Follow
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </>
    );
  }
}

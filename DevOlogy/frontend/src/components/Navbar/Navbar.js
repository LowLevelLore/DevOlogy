import React, { Component } from "react";
import "./Navbar.css";

export default class Navbar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      requestUserData: this.props.userData,
    };
  }

  render() {
    return (
      <>
        <nav>
          <div className=" logo-c left-nav">
            <a
              href="/"
              className="logo flex-v-center"
              style={{ height: "100%" }}
            >
              <img
                className="logo"
                src="/static//images/written-logo.png"
                alt="DevOlogy Logo"
              />
            </a>
          </div>
          <div className=" flex-v-center center-nav">
            <input
              type="text"
              id="search"
              placeholder="Search"
              className="git"
            />
          </div>
          <div className=" flex-v-center right-nav sb">
            <div className="icon-container">
              <a href="/">
                <img className="icon" src="/static/svgs/home.png" alt="" />
              </a>
            </div>
            <div className="icon-container">
              <a href="/chat/">
                <img
                  className="icon messenger"
                  src="/static/svgs/messenger.png"
                  alt=""
                />
              </a>
            </div>
            <div className="icon-container">
              <a href="/explore/">
                <img className="icon" src="/static/svgs/compass.png" alt="" />
              </a>
            </div>
            <div className="icon-container">
              <a href="/activities/">
                <img
                  className="icon heart"
                  src="/static/svgs/heart.svg"
                  alt=""
                />
              </a>
            </div>
            <div className="icon-container">
              <a>
                <img
                  className="icon"
                  src={this.props.userData.dp_url}
                />
              </a>
            </div>
          </div>
        </nav>

        <div
          className="container flex-h-center"
          id="srchResults"
          style={{ textAlign: "center" }}
        >
          <div className="header">
            <b>Search Here</b>
          </div>
        </div>
      </>
    );
  }
}

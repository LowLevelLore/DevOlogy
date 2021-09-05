import React, { Component } from "react";
import "./Navbar.css";

const searchInputPlaceholder = "Search";
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

export default class Navbar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      requestUserData: this.getRequestUserInfo(),
      searchValue: "",
      searchPlaceholder: searchInputPlaceholder,
      cancelOnBlur: true,
      searchDiv: null,
      isMouseInside: false,
      searchResults: {},
      showSearchHere: true,
    };
    console.log(this.state.requestUserData);
  }
  getSearchResults = async () => {
    await fetch("/api/getSearchResults/", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        Accept: "application/json",
        "X-Requested-With": "XMLHttpRequest", //Necessary to work with request.is_ajax()
        "X-CSRFToken": getCookie("csrftoken"),
      },
      credentials: "include",
      body: JSON.stringify({
        query: this.state.searchValue,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        this.setState(
          { searchResults: data.response.response },
          this.renderSearchResults
        );
      });
  };
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
        this.setState({ requestUserData: data.response }, () => {
          this.props.setUserData(data.response);
        });
        return data.response;
      });
  };
  renderSearchResults = () => {};
  componentDidMount() {
    this.setState({ searchDiv: document.getElementById("srchResults") });
  }
  handleSearchOnChange = (e) => {
    if (document.getElementById("results").innerHTML === ""){this.setState({showSearchHere: true})}
    else{this.setState({showSearchHere: false})}
    this.setState({ searchValue: e.target.value }, () => {
      this.getSearchResults();
    });
  };
  handleSearchOnFocus = () => {
    this.setState({ searchPlaceholder: "" });
    this.state.searchDiv.style.display = "block";
  };
  handleSearchOnBlur = () => {
    if (this.state.searchValue.length === 0) {
      this.setState({ searchPlaceholder: searchInputPlaceholder });
    } else {
      this.setState({ searchPlaceholder: this.state.searchValue });
    }

    if (!this.state.isMouseInside) {
      this.state.searchDiv.style.display = "none";
    }
  };
  render() {
    return (
      <>
        <nav>
          <div className="leftNav">
            <a href="/">
              <img src="/static/images/written-logo.png" alt="" />
            </a>
          </div>
          <div className="centerNav">
            <input
              type="text"
              value={this.state.searchValue}
              onChange={this.handleSearchOnChange}
              placeholder={this.state.searchPlaceholder}
              onFocus={this.handleSearchOnFocus}
              onBlur={this.handleSearchOnBlur}
            />
          </div>
          <div className="rightNav">
            <div className="icon-div">
              <img className="icon" src="/static/svgs/home.png" alt="" />
            </div>
            <div className="icon-div">
              <img className="icon" src="/static/svgs/messenger.png" alt="" />
            </div>
            <div className="icon-div">
              <img className="icon" src="/static/svgs/compass.png" alt="" />
            </div>
            <div className="icon-div">
              <img className="icon" src="/static/svgs/heart.svg" alt="" />
            </div>
            <div className="icon-div">
              <img
                className="icon"
                src={this.state.requestUserData.dp_url}
                alt=""
              />
            </div>
          </div>
        </nav>

        <div
          className="container flex-h-center"
          id="srchResults"
          style={{ display: "none", textAlign: "center" }}
          onMouseLeave={() => this.setState({ isMouseInside: false })}
          onMouseEnter={() => this.setState({ isMouseInside: true })}
        >
          <div className="header">
            {this.state.showSearchHere ? <b>Search Here</b> : ""}
          </div>
          <div id="results">
            {Object.keys(this.state.searchResults).length > 0
              ? Object.keys(this.state.searchResults).map((key) => (
                  <a className="link" href={this.state.searchResults[key].link} key={this.state.searchResults[key].username}>
                    <div className="rectangle row">
                      <div className="dp col-2">
                        <img
                          className="searchImage"
                          src={this.state.searchResults[key].image}
                          alt={this.state.searchResults[key] + "'s image"}
                        />
                      </div>

                      <div className="name col-8">
                        <div className="container name-upper">
                          {this.state.searchResults[key].username}
                        </div>
                        <div className="container name-lower">
                          {this.state.searchResults[key].full_name}
                        </div>
                      </div>
                    </div>
                  </a>
                ))
              : "No Results Found"}
          </div>
        </div>
      </>
    );
  }
}

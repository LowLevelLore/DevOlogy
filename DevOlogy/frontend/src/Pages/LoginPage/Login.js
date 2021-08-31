import React, { Component } from "react";
import "./Login.css";

// Just for getting CSRF
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const email_placeholder = "Email Or Username";
const password_placeholder = "Password";

export default class Login extends Component {
  constructor() {
    super();
    this.state = {
      username_email: "",
      password: "",
      email_placeholder: email_placeholder,
      password_placeholder: password_placeholder,
      isUserNameValid: true,
      isPasswordValid: true,
      disableLoginButton: true,
    };
    this.handleUsernameChange = this.handleUsernameChange.bind(this);
    this.handlePasswordChange = this.handlePasswordChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.isDataValid = this.isDataValid.bind(this);
  }
  handleUsernameChange(e) {
    this.setState({ username_email: e.target.value }, () => {
      this.setState({ isUserNameValid: true });
    });
  }
  handlePasswordChange(e) {
    this.setState({ password: e.target.value }, () => {
      if (!this.isDataValid()) {
        this.setState({ isPasswordValid: false });
      }
    });
  }
  isDataValid() {
    if (this.state.password.length >= 8) {
      this.setState({ disableLoginButton: false, isPasswordValid: true });
    } else {
      this.setState({ disableLoginButton: true });
    }
    return this.state.password.length >= 8;
  }
  handleSubmit(e) {
    if (this.isDataValid()) {
      e.preventDefault();
      fetch("/login/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          Accept: "application/json",
          "X-Requested-With": "XMLHttpRequest", //Necessary to work with request.is_ajax()
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          username: this.state.username_email,
          password: this.state.password,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.IsLoginSuccessful) {
            window.location.pathname = "/";
          } else {
            this.setState({ isPasswordValid: false, isUserNameValid: false });
          }
        });
    }
  }
  render() {
    return (
      <div className="main">
        <div className="container">
          <div className="white-box flex-h-center" id="main">
            <div className="container-fluid logo-c flex-h-center">
              <img id="logo" src="/static/images/written-logo.png" alt="" />
            </div>
            <div className="err">
              <span id="err"></span>
            </div>
            <div className="container-fluid form flex-h-center">
              <form
                onSubmit={this.handleSubmit}
                method="post"
                className="container-fluid form flex-h-center"
              >
                {/* {% csrf_token %} */}
                <div className="container-fluid flex-h-center">
                  {" "}
                  <input
                    id="email"
                    type="text"
                    value={this.state.username_email}
                    name="username_email"
                    onChange={this.handleUsernameChange}
                    placeholder={this.state.email_placeholder}
                    className={`form-content validate ${
                      !this.state.isUserNameValid ? "err" : ""
                    }`}
                    onFocus={() => {
                      this.setState({ email_placeholder: "" });
                    }}
                    onBlur={() => {
                      this.setState({ email_placeholder: email_placeholder });
                    }}
                  />
                </div>
                <div className="container-fluid flex-h-center">
                  {" "}
                  <input
                    type="password"
                    name="password"
                    value={this.state.password}
                    onChange={this.handlePasswordChange}
                    placeholder={this.state.password_placeholder}
                    className={`form-content validate ${
                      !this.state.isPasswordValid ? "err" : ""
                    }`}
                    onFocus={() => {
                      this.setState({ password_placeholder: "" });
                    }}
                    onBlur={() => {
                      this.setState({
                        password_placeholder: password_placeholder,
                      });
                    }}
                    id="password"
                  />
                </div>
                <button
                  type="submit"
                  className="btn btn-primary form-content"
                  id="sub-btn"
                  disabled={this.state.disableLoginButton}
                >
                  Log In
                </button>
              </form>
            </div>
            <div className="container-fluid extras">
              <div className="row">
                <div className="col-5 flex-v-center">
                  <hr width="100%" />
                </div>
                <div
                  className="col-2 flex-v-center"
                  style={{ textAlign: "center" }}
                >
                  OR
                </div>
                <div className="col-5 flex-v-center">
                  <hr width="100%" />
                </div>
              </div>
              <div className="fb-btn flex-v-center">
                <a
                  className="form-content"
                  href="{% url 'social:begin' 'facebook' %}"
                >
                  <button className="btn btn-primary">
                    Login with Facebook
                  </button>
                </a>
              </div>
              <div
                className="container-fluid"
                style={{
                  textAlign: "right",
                  fontSize: "15px",
                  margin: "10px auto",
                }}
              >
                <a href="/auth/password/reset" className="normalize-link">
                  Forgot Password ?{" "}
                </a>
              </div>
            </div>
          </div>
          <div
            className="white-box flex-h-center"
            style={{ textAlign: "center" }}
            id="signup"
          >
            <div>
              Don't have an Account ?{" "}
              <a
                href="/signup/"
                className="normalize-link"
                style={{ marginLeft: "8px" }}
              >
                Sign Up
              </a>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

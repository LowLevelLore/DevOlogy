import React, { Component } from "react";
import "./SignUp.css";

const email_placeholder = "Email";
const username_placeholder = "Username";
const name_placeholder = "Name";
const password_placeholder = "Password";

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

export default class SignUp extends Component {
  constructor() {
    super();
    this.state = {
      email_placeholder: email_placeholder,
      username_placeholder: username_placeholder,
      name_placeholder: name_placeholder,
      password_placeholder: password_placeholder,
      isEmailValid: false,
      isPasswordValid: false,
      isNameValid: false,
      isUserNameValid: false,
      email: "",
      username: "",
      password: "",
      name: "",
      showEmailError: false,
      showNameError: false,
      showPasswordError: false,
      canSubmit: false,
      userNameError: "",
      showUserNameError: false,
    };
  }

  validateEmail = async () => {
    if (this.state.email.length === 0) {
      this.setState({
        isEmailValid: false,
        showEmailError: false,
        canSubmit: false,
      });
    } else {
      await fetch("/api/isEmailAvailable/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          Accept: "application/json",
          "X-Requested-With": "XMLHttpRequest", //Necessary to work with request.is_ajax()
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          email: this.state.email,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.response) {
            this.setState({ isEmailValid: true, showEmailError: false });
          } else if (!data.response) {
            this.setState({ isEmailValid: false, showEmailError: true });
          }
          this.toggleCanSubmit();
        });
    }
  };

  validateUserName = async () => {
    if (this.state.username.length === 0) {
      this.setState({
        isUserNameValid: false,
        showUserNameError: false,
        canSubmit: false,
      });
    } else {
      await fetch("/api/isUserNameAvailable/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          Accept: "application/json",
          "X-Requested-With": "XMLHttpRequest", //Necessary to work with request.is_ajax()
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          username: this.state.username,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.response) {
            this.setState({ isUserNameValid: true, showUserNameError: false });
          } else if (!data.response) {
            this.setState({
              isUserNameValid: false,
              showUserNameError: true,
              userNameError: data.error,
            });
          }
          this.toggleCanSubmit();
        });
    }
  };

  validatePassword = () => {
    if (this.state.password.length === 0) {
      this.setState({
        isPasswordValid: false,
        showPasswordError: false,
        canSubmit: false,
      });
    } else {
      if (this.state.password.length >= 8) {
        this.setState(
          { isPasswordValid: true, showPasswordError: false },
          this.toggleCanSubmit
        );
      } else {
        this.setState(
          { isPasswordValid: false, showPasswordError: true },
          this.toggleCanSubmit
        );
      }
    }
  };

  validateName = () => {
    let isValid = (this.state.name.length >= 3 && this.state.name.length <= 40)
    this.setState({isNameValid: isValid, showNameError: this.state.name.length === 0 ? false : !isValid}, this.toggleCanSubmit)
  };

  handleEmailChange = (e) => {
    this.setState({ email: e.target.value }, this.validateEmail);
  };
  handlePasswordChange = (e) => {
    this.setState({ password: e.target.value }, this.validatePassword);
  };
  handleUserNameChange = (e) => {
    this.setState({ username: e.target.value }, this.validateUserName);
  };
  handleNameChange = (e) => {
    this.setState({ name: e.target.value }, this.validateName);
  };
  toggleCanSubmit = () => {
    if (
      this.state.isEmailValid &&
      this.state.isUserNameValid &&
      this.state.isNameValid &&
      this.state.isPasswordValid
    ) {
      this.setState({ canSubmit: true });
    } else {
      this.setState({ canSubmit: false });
    }
  };

  render() {
    return (
      <div className="container">
        <div className="white-box flex-h-center" id="main">
          <div className="container-fluid logo-c flex-h-center">
            <img id="logo" src="/static/images/written-logo.png" alt="" />
          </div>
          <div className="err">
            <span id="err"></span>
          </div>
          <div className="container-fluid form flex-h-center">
            <form method="post" className="container-fluid form flex-h-center">
              <div className="container-fluid flex-v-center">
                {" "}
                <input
                  id="email"
                  type="email"
                  name="email"
                  value={this.state.email}
                  onChange={this.handleEmailChange}
                  placeholder={this.state.email_placeholder}
                  className="form-content"
                  onFocus={() => {
                    this.setState({ email_placeholder: "" });
                  }}
                  onBlur={() => {
                    this.setState(
                      {
                        email_placeholder: email_placeholder,
                      },
                      this.validateEmail
                    );
                  }}
                />
                <div
                  className="form-content-err"
                  id="email-err"
                  style={{
                    display: `${!this.state.showEmailError ? "none" : "block"}`,
                  }}
                >
                  <img src="/static/images/error.png" width="100%" />
                </div>
              </div>
              <div className="container-fluid flex-v-center">
                {" "}
                <input
                  id="username"
                  type="text"
                  name="username"
                  value={this.state.username}
                  onChange={this.handleUserNameChange}
                  placeholder={this.state.username_placeholder}
                  className="form-content"
                  onFocus={() => {
                    this.setState({ username_placeholder: "" });
                  }}
                  onBlur={() => {
                    this.setState(
                      {
                        username_placeholder: username_placeholder,
                      },
                      this.validateUserName
                    );
                  }}
                />
                <div
                  className="form-content-err"
                  id="username-err"
                  style={{
                    display: `${
                      !this.state.showUserNameError ? "none" : "block"
                    }`,
                  }}
                >
                  <img src="/static/images/error.png" width="100%" />
                </div>
              </div>
              <div
                className="container-fluid flex-v-center small-error"
                style={{
                  display: `${this.state.showUserNameError ? "flex" : "none"}`,
                }}
              >
                {this.state.userNameError}
              </div>
              <div className="container-fluid flex-v-center">
                {" "}
                <input
                  id="name"
                  type="text"
                  name="full_name"
                  value={this.state.name}
                  onChange={this.handleNameChange}
                  placeholder={this.state.name_placeholder}
                  className="form-content"
                  onFocus={() => {
                    this.setState({ name_placeholder: "" });
                  }}
                  onBlur={() => {
                    this.setState(
                      { name_placeholder: name_placeholder },
                      this.validateName
                    );
                  }}
                />
                <div
                  className="form-content-err"
                  id="name-err"
                  style={{
                    display: `${!this.state.showNameError ? "none" : "block"}`,
                  }}
                >
                  <img src="/static/images/error.png" width="100%" />
                </div>
              </div>
              <div className="container-fluid flex-v-center">
                {" "}
                <input
                  type="password"
                  name="password"
                  value={this.state.password}
                  onChange={this.handlePasswordChange}
                  placeholder={this.state.password_placeholder}
                  className="form-content"
                  onFocus={() => {
                    this.setState({ password_placeholder: "" });
                  }}
                  onBlur={() => {
                    this.setState(
                      {
                        password_placeholder: password_placeholder,
                      },
                      this.validatePassword
                    );
                  }}
                  id="password"
                />
                <div
                  id="pass-err"
                  className="form-content-err"
                  style={{
                    display: `${
                      !this.state.showPasswordError ? "none" : "block"
                    }`,
                  }}
                >
                  <img src="/static/images/error.png" width="100%" />
                </div>
              </div>
              <button
                type="submit"
                className="btn btn-primary form-content"
                id="sub-btn"
                disabled={!this.state.canSubmit}
              >
                Sign Up
              </button>
            </form>
          </div>
          <div className="container-fluid extras">
            <div className="row mt-2">
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
                href="/auth/social-core/login/facebook/"
                disabled={true}
              >
                <button className="btn btn-primary">Login with Facebook</button>
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
            Already have an Account ?{" "}
            <a
              href="/auth/login"
              className="normalize-link"
              style={{ marginLeft: "8px" }}
            >
              Log In
            </a>
          </div>
        </div>
      </div>
    );
  }
}

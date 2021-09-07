import React, { Component } from 'react'
import "./Post.css"

export default class Post extends Component {
    constructor(props){
        super(props);
        this.state = {};
    }
    render() {
        return (
            <div>
                {this.props.username}
            </div>
        )
    }
}

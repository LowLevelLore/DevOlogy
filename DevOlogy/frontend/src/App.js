import ReactDOM from 'react-dom'
import React, {Component} from 'react'
import { BrowserRouter as Router , Route, Switch } from 'react-router-dom'


class App extends Component {
    render() {
        return (
            <>
            <p>Hello</p>
            </>
        )
    }
}

ReactDOM.render(<App />, document.getElementById('app'))
export default App;

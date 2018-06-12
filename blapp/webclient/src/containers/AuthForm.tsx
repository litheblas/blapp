import * as React from 'react'
import * as R from 'ramda'
import { Button, Container, Row, Col } from 'reactstrap'
import { Dispatch, Action } from 'redux'
import { connect } from 'react-redux'
import { actionTypes, actions } from '../actions'

const mapStateToProps = (state: any, ownProps: Object) => ({
  token: state.auth.token,
})

const mapDispatchToProps = (dispatch: Dispatch, ownProps: Object) => ({
  setAuthToken: (token: string) => dispatch({type: actionTypes.setAuthToken, payload: token}),
})

interface AuthFormState {
  token: string,
}

export const AuthFormContainer = connect(mapStateToProps, mapDispatchToProps)(
  class extends React.Component<any, AuthFormState> {
    constructor(props: any) {
      super(props)

      this.state = {
        token: props.token,
      }

      this.setState = this.setState.bind(this)
      this.submit = this.submit.bind(this)
    }

    submit(e: React.FormEvent<HTMLFormElement>) {
      this.props.setAuthToken(this.state.token)
      e.preventDefault()
    }

    render() {
      return <>
        <form onSubmit={this.submit}>
          <input type='text' value={this.state.token} onChange={(e) => this.setState({token: e.target.value})} />
          <input type='submit' />
        </form>
      </>
    }
  }
)

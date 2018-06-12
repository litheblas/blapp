import * as React from 'react'
import * as R from 'ramda'
import { Button, Container, Row, Col } from 'reactstrap'
import { Dispatch, Action } from 'redux'
import { connect } from 'react-redux'
import { actionTypes, actions } from '../actions'

import { BulkSellerContainer } from './BulkSeller'
import { AuthFormContainer } from './AuthForm'

import 'bootstrap/dist/css/bootstrap.css'


const mapStateToProps = (state: any, ownProps: Object) => ({
  isAuthenticated: state.auth.isAuthenticated,
  token: state.auth.token,
})

const mapDispatchToProps = (dispatch: Dispatch, ownProps: Object) => ({
  //@ts-ignore
  getBaseData: () => dispatch(actions.getBaseData()),
  setAuthToken: (token: string) => dispatch({type: actionTypes.setAuthToken, payload: token}),
})

export const AppContainer = connect(mapStateToProps, mapDispatchToProps)(
  class extends React.Component<any> {
    componentDidMount() {
      this.props.getBaseData()
    }

    render() {
      return this.props.isAuthenticated ? <>
        <BulkSellerContainer />
      </> : <>
        <AuthFormContainer />
      </>
    }
  }
)

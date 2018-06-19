import * as React from 'react'
import { Dispatch } from 'redux'
import { connect } from 'react-redux'

import { actionTypes, actions } from 'blapp/commerce/actions'
import { AuthFormContainer } from 'blapp/commerce/containers/AuthForm'
import { BulkSellerContainer } from 'blapp/commerce/containers/BulkSeller'

import 'blapp/style'

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

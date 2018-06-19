import * as R from 'ramda'

import { actionTypes } from 'blapp/commerce/actions'

const defaultState = {
  offline: {},
  auth: {
    isAuthenticated: false,
    token: '',
  },
  selectedProduct: '',
  selectedSalePoint: '',
  people: {},
  purchases: {},
  failedPurchases: {},
  salePoints: {},
}

const edgeListToObject = (list: any) => R.pipe(
  R.pluck('node'),
  R.map((x: any) => [x.id, x]),
  R.fromPairs,
)(list)

const reducer = (state = defaultState, action: any) => {
  switch (action.type) {
    case actionTypes.setAuthToken:
      return {
        ...state,
        auth: {
          ...state.auth,
          token: action.payload,
          isAuthenticated: true,
        }
      }
    case actionTypes.getBaseData.commit:
      return {
        ...state,
        people: edgeListToObject(action.payload.data.people.edges),
        products: edgeListToObject(action.payload.data.products.edges),
        purchases: edgeListToObject(action.payload.data.purchases.edges),
        salePoints: edgeListToObject(action.payload.data.salePoints.edges),
        selectedProduct: R.values(action.payload.data.products.edges)[0].node.id,
        selectedSalePoint: R.values(action.payload.data.salePoints.edges)[0].node.id,
      }
    case actionTypes.getBaseData.rollback:
      return {
        ...state,
        auth: {
          ...state.auth,
          isAuthenticated: false,
        },
      }
    case actionTypes.makePurchase.commit:
      return {
        ...state,
        purchases: {
          ...state.purchases,
          [action.payload.data.makePurchase.purchase.id]: action.payload.data.makePurchase.purchase,
        },
      }
    case actionTypes.makePurchase.rollback:
      return {
        ...state,
        failedPurchases: {
          ...state.failedPurchases,
          [action.meta.purchase.uid]: action.meta.purchase
        },
      }
    default:
      return state
  }
}

export default reducer

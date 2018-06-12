import * as R from 'ramda'
import uuid1 from 'uuid/v1'
import uuid4 from 'uuid/v4'
import { DateTime } from 'luxon'
import { ThunkAction } from 'redux-thunk';

const subActionSeparator = '/'

export interface SubActionNameSuffixMap {
  [x: string]: string,
}
const defaultSubActionNameSuffixMap = {
  request: '',
  commit: `${subActionSeparator}commit`,
  rollback: `${subActionSeparator}rollback`,
}

const offlineActionType = (
  baseActionName: string,
  subActionNameSuffixMap: SubActionNameSuffixMap = defaultSubActionNameSuffixMap
): SubActionNameSuffixMap => (
  R.map((subActionSuffix) => (baseActionName + subActionSuffix), subActionNameSuffixMap)
)

export const actionTypes = {
  setAuthToken: 'setAuthToken',
  getBaseData: offlineActionType('getBaseData'),
  makePurchase: offlineActionType('makePurchase'),
}

const getBaseData = () => (dispatch: any, getState: any) => {
  dispatch({
    type: actionTypes.getBaseData.request,
    payload: {},
    meta: {
      offline: {
        effect: {
          url: '/api/graphql/',
          method: 'POST',
          body: JSON.stringify({
            query: `
              query {
                people(tempTour18: true) {
                  edges {
                    node {
                      id
                      fullName
                      shortName
                    }
                  }
                }
                salePoints {
                  edges {
                    node {
                      id
                      name
                    }
                  }
                }
                products {
                  edges {
                    node {
                      id
                      name
                    }
                  }
                }
                purchases {
                  edges {
                    node {
                      id
                      uid
                      salePoint {
                        id
                      }
                      product {
                        id
                      }
                      person {
                        id
                      }
                      timestamp
                      quantity
                    }
                  }
                }
              }
            `,
            variables: null,
          }),
          headers: {
            'Authorization': `Service-Token ${getState().auth.token}`,
          },
        },
        commit: {
          type: actionTypes.getBaseData.commit,
        },
        rollback: {
          type: actionTypes.getBaseData.rollback,
        },
      }
    }
  })
}

const makePurchase = (salePointId: string, productId: string, personId: string, timestamp: DateTime, quantity: number) => (dispatch: any, getState: any) => {
  const clientMutationId = uuid4()
  const uid = uuid1()

  const meta = {
    uid,
    salePoint: salePointId,
    product: productId,
    person: personId,
    timestamp: timestamp,
    quantity: quantity,
  }

  dispatch({
    type: actionTypes.makePurchase.request,
    payload: {
      uid,
    },
    meta: {
      purchase: meta,
      offline: {
        effect: {
          url: '/api/graphql/',
          method: 'POST',
          body: JSON.stringify({
            query: `
              mutation ($input: MakePurchaseInput!) {
                makePurchase(input: $input) {
                  purchase {
                    id
                    uid
                    salePoint {
                      id
                    }
                    product {
                      id
                    }
                    person {
                      id
                    }
                    timestamp
                    quantity
                  }
                }
              }
            `,
            variables: {
              input: {
                clientMutationId,
                uid,
                product: productId,
                person: personId,
                salePoint: salePointId,
                quantity,
                timestamp: timestamp.toISO(),
              }
            }
          }),
          headers: {
            'Authorization': `Service-Token ${getState().auth.token}`,
          },
        },
        commit: {
          type: actionTypes.makePurchase.commit,
          meta: {
            purchase: meta,
          },
        },
        rollback: {
          type: actionTypes.makePurchase.rollback,
          meta: {
            purchase: meta,
          },
        },
      }
    }
  })
}

export const actions = {
  getBaseData,
  makePurchase,
}

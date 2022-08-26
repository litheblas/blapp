import * as R from 'ramda'
import { v1 as uuid1 } from 'uuid'
import { v4 as uuid4 } from 'uuid'
import { DateTime } from 'luxon'

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

const makePurchase = (salePointId: string, productId: string, personId: string, timestamp: DateTime, quantity: number, uid: string = uuid1()) => (dispatch: any, getState: any) => {
  const clientMutationId = uuid4()

  const meta = {
    uid,
    salePoint: {
      id: salePointId,
    },
    product: {
      id: productId,
    },
    person: {
      id: personId,
    },
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

const retryAllFailedPurchases = () => (dispatch: any, getState: any) => {
  R.values(getState().failedPurchases).forEach((p) => {
    dispatch(makePurchase(
      p.salePoint.id,
      p.product.id,
      p.person.id,
      DateTime.fromISO(p.timestamp),
      p.quantity,
      p.uid,
    ))
  })
}

export const actions = {
  getBaseData,
  makePurchase,
  retryAllFailedPurchases,
}

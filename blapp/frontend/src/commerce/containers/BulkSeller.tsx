import * as React from 'react'
import * as R from 'ramda'
import { Button, Container, Row, Col, Table } from 'reactstrap'
import { Dispatch, AnyAction } from 'redux'
import { connect } from 'react-redux'
import { DateTime } from 'luxon'

import { actions, actionTypes } from '../actions'

interface BulkSellerState {
  personId: string | null,
  quantity: number | null,
}

const quantities = R.range(0,51).map(x => x * 2)

const fixPurchases = R.pipe(
  R.values,
  //@ts-ignore
  R.sortBy(R.pluck('timestamp')),
  R.reverse,
)

const mapStateToProps = (state: any, ownProps: any) => ({
  people: state.people,
  purchases: state.purchases,
  failedPurchases: state.failedPurchases,
  //@ts-ignore
  unsyncedPurchases: state.offline.outbox.filter((x) => x.type === actionTypes.makePurchase.request).map((x) => x.meta.purchase),
  selectedProductId: state.selectedProduct,
  selectedSalePointId: state.selectedSalePoint,
})

const mapDispatchToProps = (dispatch: Dispatch, ownProps: any) => ({
  //@ts-ignore
  makePurchase: (salePointId: string, productId: string, personId: string, timestamp: DateTime, quantity: number) => dispatch(actions.makePurchase(salePointId, productId, personId, timestamp, quantity)),
})

export const BulkSellerContainer = connect(mapStateToProps, mapDispatchToProps)(
  class extends React.Component<any, BulkSellerState> {
    constructor(props: any) {
      super(props)

      this.state = {
        personId: null,
        quantity: null,
      }

      this.makePurchase = this.makePurchase.bind(this)
    }

    makePurchase() {
      this.props.makePurchase(
        this.props.selectedSalePointId,
        this.props.selectedProductId,
        this.state.personId,
        DateTime.utc(),
        this.state.quantity,
      )

      this.setState({
        personId: null,
        quantity: null,
      })
    }

    render() {
      return <>
        <Container fluid style={{marginTop: '15px'}}>
          <Row>
            <Col sm={2}>
              <Row>
                {quantities.map((quantity, quantityKey) => (
                  <Col xs={12} className='mb-2' key={quantityKey}>
                    <Button block size='md' className='py-3' color={this.state.quantity === quantity ? 'success' : 'secondary'} onClick={() => this.setState({quantity})}>{quantity}</Button>
                  </Col>
                ))}
              </Row>
            </Col>
            <Col sm={6}>
              <Row>
                {R.pipe(
                  R.values,
                  R.sortBy((x) => x.shortName),
                  R.mapObjIndexed((person: any, personKey: any) => (
                    <Col sm={3} className='mb-2' key={personKey}>
                      <Button block size='md' className='py-3' color={this.state.personId === person.id ? 'success' : 'secondary'} onClick={() => this.setState({personId: person.id})}>{person.shortName}</Button>
                    </Col>
                  )),
                  R.values,
                )(this.props.people)}
              </Row>
            </Col>
            <Col sm={4}>
              <Button block size='lg' className='py-4' color='primary' disabled={!(this.state.personId && this.state.quantity)} onClick={this.makePurchase}>Köp</Button>
              <p></p>
              <h3>Osynkade köp</h3>
              <Table size='sm'>
                <thead>
                  <tr>
                    <th>Person</th>
                    <th>Kvantitet</th>
                    <th>Tidsstämpel</th>
                  </tr>
                </thead>
                <tbody>
                  {
                    //@ts-ignore
                    fixPurchases(this.props.unsyncedPurchases).map((purchase: any, purchaseKey: any) => (
                      <tr key={purchaseKey}>
                        <td>{typeof this.props.people[purchase.person.id] != 'undefined' ? this.props.people[purchase.person.id].shortName : 'Okänd'}</td>
                        <td>{purchase.quantity}</td>
                        <td>{DateTime.fromISO(purchase.timestamp).setLocale('sv-SE').toLocaleString(DateTime.DATETIME_SHORT_WITH_SECONDS)}</td>
                      </tr>
                    ))
                  }
                </tbody>
              </Table>

              <h3>Misslyckade köp</h3>
              <Table size='sm'>
                <thead>
                  <tr>
                    <th>Person</th>
                    <th>Kvantitet</th>
                    <th>Tidsstämpel</th>
                  </tr>
                </thead>
                <tbody>
                  {
                    //@ts-ignore
                    fixPurchases(this.props.failedPurchases).map((purchase: any, purchaseKey: any) => (
                      <tr key={purchaseKey}>
                        <td>{typeof this.props.people[purchase.person.id] != 'undefined' ? this.props.people[purchase.person.id].shortName : 'Okänd'}</td>
                        <td>{purchase.quantity}</td>
                        <td>{DateTime.fromISO(purchase.timestamp).setLocale('sv-SE').toLocaleString(DateTime.DATETIME_SHORT_WITH_SECONDS)}</td>
                      </tr>
                    ))
                  }
                </tbody>
              </Table>

              <h3>Synkade köp</h3>
              <Table size='sm'>
                <thead>
                  <tr>
                    <th>Person</th>
                    <th>Kvantitet</th>
                    <th>Tidsstämpel</th>
                  </tr>
                </thead>
                <tbody>
                  {
                    //@ts-ignore
                    fixPurchases(this.props.purchases).map((purchase: any, purchaseKey: any) => (
                      <tr key={purchaseKey}>
                        <td>{typeof this.props.people[purchase.person.id] != 'undefined' ? this.props.people[purchase.person.id].shortName : 'Okänd'}</td>
                        <td>{purchase.quantity}</td>
                        <td>{DateTime.fromISO(purchase.timestamp).setLocale('sv-SE').toLocaleString(DateTime.DATETIME_SHORT_WITH_SECONDS)}</td>
                      </tr>
                    ))
                  }
                </tbody>
              </Table>

            </Col>
          </Row>
        </Container>
      </>
    }
  }
)

import * as React from 'react'
import * as R from 'ramda'
import { Button, Container, Row, Col, Table } from 'reactstrap'
import { Dispatch, AnyAction } from 'redux'
import { connect } from 'react-redux'
import { DateTime } from 'luxon'

import { actions } from '../actions'

interface BulkSellerState {
  personId: string | null,
  quantity: number | null,
}

const quantities = R.range(0,51).map(x => x * 2)

const mapObj = (fn: any) => R.pipe(
  R.mapObjIndexed(fn),
  R.values,
)

const mapObjSortBy = (mapFn: any, sortFn: any) => R.pipe(
  R.mapObjIndexed(mapFn),
  R.values,
  R.sortBy(sortFn),
)

const mapStateToProps = (state: any, ownProps: any) => ({
  people: state.people,
  purchases: state.purchases,
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
        <Container fluid>
          <Row>
            <Col sm={2}>
              <Row>
                {quantities.map((quantity, quantityKey) => (
                  <Col xs={12} className='mb-2' key={quantityKey}>
                    <Button block size='lg' className='py-3' color={this.state.quantity === quantity ? 'success' : 'default'} onClick={() => this.setState({quantity})}>{quantity}</Button>
                  </Col>
                ))}
              </Row>
            </Col>
            <Col sm={7}>
              <Row>
                {mapObjSortBy((person: any, personKey: any) => (
                  <Col sm={3} className='mb-2' key={personKey}>
                    <Button block size='lg' className='py-3' color={this.state.personId === person.id ? 'success' : 'default'} onClick={() => this.setState({personId: person.id})}>{person.shortName}</Button>
                  </Col>
                ), (x: any) => x.shortName)(this.props.people)}
              </Row>
            </Col>
            <Col sm={3}>
              <Button block size='lg' className='py-3' onClick={this.makePurchase}>Köp</Button>
              <Table size='sm'>
                <thead>
                  <tr>
                    <th>Person</th>
                    <th>Kvantitet</th>
                    <th>Tidsstämpel</th>
                  </tr>
                </thead>
                <tbody>
                  {R.reverse(mapObjSortBy((purchase: any, purchaseKey: any) => (
                    <tr>
                      <td>{this.props.people[purchase.person.id].shortName}</td>
                      <td>{purchase.quantity}</td>
                      <td>{DateTime.fromISO(purchase.timestamp).setLocale('sv-SE').toLocaleString(DateTime.DATETIME_SHORT_WITH_SECONDS)}</td>
                    </tr>
                  ), (x: any) => x.timestamp)(this.props.purchases))}
                </tbody>
              </Table>

            </Col>
          </Row>
        </Container>
      </>
    }
  }
)

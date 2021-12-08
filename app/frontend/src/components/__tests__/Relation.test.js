import React from 'react'
import { expect, test, beforeEach, describe, jest } from '@jest/globals'
import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import userEvent from '@testing-library/user-event'
import configureStore from 'redux-mock-store'
import { Provider } from 'react-redux'
import { Relation } from '../Relation'
import { relReducer } from '../../store/relations/reducers'

const mockStore = configureStore([])

const relation = {
	id: '{"type":"relation","value":3}',
	name1: '{"type":"db_structured_name","value":4422}',
	name2: '{"type":"structured_name","value":2}',
	belongs_to: 0,
	reference_id: -1,
	formattedName1: 'Basisletta / Member / Norway',
	formattedName2: 'Abercwmeiddaw / Formation / Saskatchewan',
}

describe('When relation without inclusion rendered', () => {
	let store
	beforeEach(() => {
		store = mockStore({
			rel: relReducer([], { type: 'INIT', rel: {} }),
		})
		store.dispatch = jest.fn()
		render(
			<Provider store={store}>
				<table>
					<tbody>
						<Relation
							relation={relation}
							formattedName1={relation.formattedName1}
							formattedName2={relation.formattedName2}
						/>
					</tbody>
				</table>
			</Provider>
		)
	})

	test('shows "swap" button', () => {
		const swapButton = screen.getByRole('button')
		expect(swapButton).toBeInTheDocument()
	})

	test('shows structured names forming a relation on the same row', () => {
		const relationRow = screen.getByRole('row', {
			name: `${relation.formattedName1} ↔ ${relation.formattedName2}`,
		})
		expect(relationRow).toBeInTheDocument()
	})

	test('swaps relations on "swap" button press', () => {
		const swapButton = screen.getByRole('button')
		userEvent.click(swapButton)
		expect(store.dispatch).toHaveBeenCalledTimes(1)
		expect(store.dispatch).toHaveBeenCalledWith({
			type: 'UPDATE',
			rel: {
				...relation,
				name1: relation.name2,
				name2: relation.name1,
			},
		})
	})

	test('has "belongs to" checkbox', () => {
		const belongToCheckbox = screen.getByRole('checkbox')
		expect(belongToCheckbox).toBeInTheDocument()
	})

	test('creates inclusion on "belongs to" button click', () => {
		const belongToCheckbox = screen.getByRole('checkbox')
		userEvent.click(belongToCheckbox)
		expect(store.dispatch).toHaveBeenCalledTimes(1)
		expect(store.dispatch).toHaveBeenCalledWith({
			type: 'UPDATE',
			rel: {
				...relation,
				belongs_to: 1,
			},
		})
	})
})

describe('When relation with inclusion rendered', () => {
	let store
	const relationWithInclusion = { ...relation, belongs_to: 1 }
	beforeEach(() => {
		store = mockStore({
			rel: relReducer([], { type: 'INIT', rel: {} }),
		})
		store.dispatch = jest.fn()
		render(
			<Provider store={store}>
				<table>
					<tbody>
						<Relation
							relation={relationWithInclusion}
							formattedName1={relation.formattedName1}
							formattedName2={relation.formattedName2}
						/>
					</tbody>
				</table>
			</Provider>
		)
	})

	test('removes inclusion on "belongs to" button click', () => {
		const belongToCheckbox = screen.getByRole('checkbox')
		userEvent.click(belongToCheckbox)
		expect(store.dispatch).toHaveBeenCalledTimes(1)
		expect(store.dispatch).toHaveBeenCalledWith({
			type: 'UPDATE',
			rel: {
				...relation,
				belongs_to: 0,
			},
		})
	})
})

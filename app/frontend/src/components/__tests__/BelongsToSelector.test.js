import React from 'react'
import { expect, test, beforeEach, describe, jest } from '@jest/globals'
import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import userEvent from '@testing-library/user-event'
import configureStore from 'redux-mock-store'
import { Provider } from 'react-redux'
import { BelongsToSelector } from '../BelongsToSelector'
import { makeId } from '../../utilities'

const mockStore = configureStore([])

const sname1Id = '{"type":"structured_name","value":1}'
const sname2Id = '{"type":"db_structured_name","value":4422}'
const nonInclusiveRelation = {
	id: makeId('relation'),
	name1: sname1Id,
	name2: sname2Id,
	belongs_to: 0,
	reference_id: -1,
}

describe('When pair of structured names is added, but no relations formed', () => {
	let store
	beforeEach(() => {
		store = mockStore()
		store.dispatch = jest.fn()
		render(
			<Provider store={store}>
				<BelongsToSelector idA={sname1Id} idB={sname2Id} />
			</Provider>
		)
	})

	test('shows three buttons for different inclusion options', () => {
		const rightToLeft = screen.getByText('←')
		const noInclusion = screen.getByText('↔')
		const leftToRight = screen.getByText('→')
		expect(rightToLeft).toBeInTheDocument()
		expect(noInclusion).toBeInTheDocument()
		expect(leftToRight).toBeInTheDocument()
	})

	test('no option is rendered as selected', () => {
		const rightToLeft = screen.getByText('←')
		const noInclusion = screen.getByText('↔')
		const leftToRight = screen.getByText('→')
		expect(rightToLeft).toHaveClass('w3-btn w3-white')
		expect(noInclusion).toHaveClass('w3-btn w3-white')
		expect(leftToRight).toHaveClass('w3-btn w3-white')
	})

	test('creates new relation and rightToLeft inclusion on "rightToLeft" button click', () => {
		const rightToLeft = screen.getByText('←')
		userEvent.click(rightToLeft)
		expect(store.dispatch).toHaveBeenCalledTimes(1)
		expect(store.dispatch).toHaveBeenCalledWith({
			type: 'ADD',
			rel: {
				id: expect.anything(),
				name1: sname1Id,
				name2: sname2Id,
				belongs_to: 1,
				reference_id: -1,
			},
		})
	})

	test('creates new relation with no inclusion on "noInclusion" button click', () => {
		const noInclusion = screen.getByText('↔')
		userEvent.click(noInclusion)
		expect(store.dispatch).toHaveBeenCalledTimes(1)
		expect(store.dispatch).toHaveBeenCalledWith({
			type: 'ADD',
			rel: {
				id: expect.anything(),
				name1: sname1Id,
				name2: sname2Id,
				belongs_to: 0,
				reference_id: -1,
			},
		})
	})

	test('creates new relation and leftToRight inclusion on "leftToRight" button click', () => {
		const leftToRight = screen.getByText('→')
		userEvent.click(leftToRight)
		expect(store.dispatch).toHaveBeenCalledTimes(1)
		expect(store.dispatch).toHaveBeenCalledWith({
			type: 'ADD',
			rel: {
				id: expect.anything(),
				name1: sname2Id,
				name2: sname1Id,
				belongs_to: 1,
				reference_id: -1,
			},
		})
	})
})

describe('When pair of structured names with non inclusive relation added', () => {
	let store
	beforeEach(() => {
		store = mockStore()
		store.dispatch = jest.fn()
		render(
			<Provider store={store}>
				<BelongsToSelector
					idA={sname1Id}
					idB={sname2Id}
					relation={nonInclusiveRelation}
				/>
			</Provider>
		)
	})

	test('shows "noInclusion" button as selected', () => {
		const noInclusion = screen.getByText('↔')
		expect(noInclusion).toHaveClass('w3-btn w3-green')
	})

	test('updates relation and creates rightToLeft inclusion on "rightToLeft" button click', () => {
		const rightToLeft = screen.getByText('←')
		userEvent.click(rightToLeft)
		expect(store.dispatch).toHaveBeenCalledTimes(1)
		expect(store.dispatch).toHaveBeenCalledWith({
			type: 'UPDATE',
			rel: {
				id: expect.anything(),
				name1: sname1Id,
				name2: sname2Id,
				belongs_to: 1,
				reference_id: -1,
			},
		})
	})

	test('updates relation and creates leftToRight inclusion on "leftToRight" button click', () => {
		const leftToRight = screen.getByText('→')
		userEvent.click(leftToRight)
		expect(store.dispatch).toHaveBeenCalledTimes(1)
		expect(store.dispatch).toHaveBeenCalledWith({
			type: 'UPDATE',
			rel: {
				id: expect.anything(),
				name1: sname2Id,
				name2: sname1Id,
				belongs_to: 1,
				reference_id: -1,
			},
		})
	})
})

describe('When pair of structured names with inclusive relation added', () => {
	const inclusiveRelation = { ...nonInclusiveRelation, belongs_to: 1 }

	test('shows "rightToLeft" button as selected when sname1 is on the left side', () => {
		const store = mockStore()
		store.dispatch = jest.fn()
		render(
			<Provider store={store}>
				<BelongsToSelector
					idA={sname1Id}
					idB={sname2Id}
					relation={inclusiveRelation}
				/>
			</Provider>
		)
		const rightToLeft = screen.getByText('←')
		expect(rightToLeft).toHaveClass('w3-btn w3-green')
	})

	test('shows "leftToRight" button as selected when sname1 is on the right side', () => {
		const store = mockStore()
		store.dispatch = jest.fn()
		render(
			<Provider store={store}>
				<BelongsToSelector
					idA={sname2Id}
					idB={sname1Id}
					relation={inclusiveRelation}
				/>
			</Provider>
		)
		const leftToRight = screen.getByText('→')
		expect(leftToRight).toHaveClass('w3-btn w3-green')
	})
})

import React from 'react'
import { expect, test, beforeEach, describe, jest } from '@jest/globals'
import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import userEvent from '@testing-library/user-event'
import configureStore from 'redux-mock-store'
import { ReferenceForm } from '../ReferenceForm'
import { Provider } from 'react-redux'
import { refReducer } from '../../store/references/reducers'
import * as utilities from '../../utilities.js'

const mockStore = configureStore([])
jest.mock('../../utilities.js')

describe('When no reference information provided, ReferenceForm', () => {
	let store
	beforeEach(() => {
		store = mockStore({
			ref: refReducer,
		})
		store.dispatch = jest.fn()
		render(
			<Provider store={store}>
				<ReferenceForm
					displayRefForm='none'
					showNewReferenceForm={() => {}}
					isQueried={true}
				/>
			</Provider>
		)
	})

	test('has submit button', () => {
		const saveReferenceBtn = screen.getByRole('button')
		expect(saveReferenceBtn).toBeInTheDocument()
		expect(saveReferenceBtn).toHaveAttribute('type', 'submit')
	})

	test('shows inputs for all reference elements', () => {
		const inputFields = screen.getAllByRole('textbox')
		expect(inputFields).toHaveLength(5)
	})

	test('does not autofill input fields', () => {
		const inputFields = screen.getAllByRole('textbox')
		expect(inputFields[0].value).toBe('')
		expect(inputFields[1].value).toBe('')
		expect(inputFields[2].value).toBe('')
		expect(inputFields[3].value).toBe('')
		expect(inputFields[4].value).toBe('')
	})

	test('reflects the user input', async () => {
		const inputFields = screen.getAllByRole('textbox')
		userEvent.type(inputFields[0], 'Úna C. Farrell')
		const firstAuthor = await screen.findByDisplayValue('Úna C. Farrell')
		expect(firstAuthor).toBeInTheDocument()
	})

	test('creats a new reference on save', async () => {
		utilities.findDuplicateDois.mockImplementationOnce(doi => [])
		utilities.findDuplicateLinks.mockImplementationOnce(doi => [])
		const inputFields = screen.getAllByRole('textbox')
		const saveReferenceBtn = screen.getByRole('button')
		userEvent.type(
			inputFields[2],
			"Beyond Beecher's Trilobite Bed: Widespread pyritization of soft tissues in the Late Ordovician Taconic foreland basin"
		)
		userEvent.click(saveReferenceBtn)
		expect(store.dispatch).toHaveBeenCalledTimes(1)
		expect(store.dispatch).toHaveBeenCalledWith({
			ref: expect.anything(),
			type: 'ADD',
		})
	})

	test('does not show "Make new doi search" button', () => {
		const makeNewDoiSearchBtn = screen.queryByRole('button', {
			name: 'Make new doi search',
		})
		expect(makeNewDoiSearchBtn).not.toBeInTheDocument()
	})
})

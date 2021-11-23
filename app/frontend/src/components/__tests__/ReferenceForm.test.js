import React from 'react'
import { expect, test, beforeEach, describe, jest } from '@jest/globals'
import { render, screen, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import userEvent from '@testing-library/user-event'
import configureStore from 'redux-mock-store'
import axios from 'axios'
import { ReferenceForm } from '../ReferenceForm'
import { Provider } from 'react-redux'
import { refReducer } from '../../store/references/reducers'
import * as utilities from '../../utilities.js'
import { foundDoiResponseData } from '../test/data/crossapiResponse'

const mockStore = configureStore([])
jest.mock('axios')
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
					displayRefForm='block'
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

	test('does not print error msg if no doi or link duplicates found', async () => {
		utilities.findDuplicateDois.mockImplementationOnce(doi => [])
		utilities.findDuplicateLinks.mockImplementationOnce(doi => [])
		const saveReferenceBtn = screen.getByRole('button')
		userEvent.click(saveReferenceBtn)
		const notification = await screen.queryByText(
			'An existing reference is using the same doi.'
		)
		expect(notification).not.toBeInTheDocument()
	})

	test('prints error msg if link duplicates found', async () => {
		utilities.findDuplicateDois.mockImplementationOnce(doi => [])
		utilities.findDuplicateLinks.mockImplementationOnce(doi => [
			{
				title: 'Katian (Ordovician) to Aeronian (Silurian, Llandovery) graptolite biostratigraphy of the\nYD\n\u20101 drill core, Yuanan County, Hubei Province, China',
				link: 'http://dx.doi.org/10.1002/spp2.1267',
			},
		])
		const saveReferenceBtn = screen.getByRole('button')
		userEvent.click(saveReferenceBtn)
		const notification = await screen.queryByText(
			'An existing reference is using the same doi.'
		)
		expect(notification).toBeInTheDocument()
	})

	test('prints error msg if doi duplicates found', async () => {
		utilities.findDuplicateDois.mockImplementationOnce(doi => [
			{
				title: 'Katian (Ordovician) to Aeronian (Silurian, Llandovery) graptolite biostratigraphy of the\nYD\n\u20101 drill core, Yuanan County, Hubei Province, China',
				doi: '10.1002/spp2.1267',
			},
		])
		utilities.findDuplicateLinks.mockImplementationOnce(doi => [])
		const saveReferenceBtn = screen.getByRole('button')
		userEvent.click(saveReferenceBtn)
		const notification = await screen.queryByText(
			'An existing reference is using the same doi.'
		)
		expect(notification).toBeInTheDocument()
	})
})

describe('When user is editing an existing reference, ReferenceForm', () => {
	let store
	const ref = {
		firstAuthor: 'Shunxin Zhang',
		year: 2018,
		title: 'The stratigraphic position and the age of the Ordovician organic-rich intervals in the northern Hudson Bay, Hudson Strait, and Foxe basins—evidence from graptolites',
		doi: '10.1139/cjes-2017-0266',
		link: 'http://dx.doi.org/10.1139/cjes-2017-0266',
		exists: false,
		queried: true,
		edit: true,
		id: '{"type":"reference","value":1}',
	}
	beforeEach(() => {
		store = mockStore({
			ref: refReducer,
		})
		store.dispatch = jest.fn()
		render(
			<Provider store={store}>
				<ReferenceForm
					reference={ref}
					displayRefForm='block'
					showNewReferenceForm={() => {}}
					isQueried={true}
				/>
			</Provider>
		)
	})

	test('has buttons for saving reference and making new doi search', () => {
		const btns = screen.getAllByRole('button')
		expect(btns).toHaveLength(2)
	})

	test('does not create a new reference on save', async () => {
		utilities.findDuplicateDois.mockImplementationOnce(doi => [])
		utilities.findDuplicateLinks.mockImplementationOnce(doi => [])
		const inputFields = screen.getAllByRole('textbox')
		const saveReferenceBtn = screen.getByRole('button', {
			name: 'Save reference',
		})
		userEvent.clear(inputFields[1])
		userEvent.type(inputFields[1], '2017')
		userEvent.click(saveReferenceBtn)
		expect(store.dispatch).toHaveBeenCalledTimes(1)
		expect(store.dispatch).not.toHaveBeenCalledWith({
			ref: expect.anything(),
			type: 'ADD',
		})
	})

	test('updates an existing reference on save', async () => {
		utilities.findDuplicateDois.mockImplementationOnce(doi => [])
		utilities.findDuplicateLinks.mockImplementationOnce(doi => [])
		const inputFields = screen.getAllByRole('textbox')
		const saveReferenceBtn = screen.getByRole('button', {
			name: 'Save reference',
		})
		userEvent.clear(inputFields[0])
		userEvent.type(inputFields[0], 'Colmenar, J.')
		userEvent.click(saveReferenceBtn)
		expect(store.dispatch).toHaveBeenCalledTimes(1)
		expect(store.dispatch).toHaveBeenCalledWith({
			ref: { ...ref, firstAuthor: 'Colmenar, J.', edit: false },
			type: 'UPDATE',
		})
	})

	test('shows new empty DoiForm on "Make new doi search" button click', async () => {
		const makeNewDoiSearchBtn = screen.queryByRole('button', {
			name: 'Make new doi search',
		})
		userEvent.click(makeNewDoiSearchBtn)
		const doiForm = await screen
			.queryByText('Manual Entry', { exact: false })
			.closest('form')
		expect(doiForm).toBeInTheDocument()
		const inputFields = screen.getAllByRole('textbox')
		expect(inputFields).toHaveLength(1)
		expect(inputFields[0].value).toBe('')
	})
})

describe('ReferenceForm validates input and', () => {
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
		utilities.findDuplicateDois.mockImplementationOnce(doi => [])
		utilities.findDuplicateLinks.mockImplementationOnce(doi => [])
	})

	test('does not print error msg if user provides correct data for reference', async () => {
		const inputFields = screen.getAllByRole('textbox')
		const saveReferenceBtn = screen.getByRole('button')
		userEvent.type(inputFields[0], 'Úna C. Farrell')
		userEvent.type(inputFields[1], '2009')
		userEvent.type(
			inputFields[2],
			"Beyond Beecher's Trilobite Bed: Widespread pyritization of soft tissues in the Late Ordovician Taconic foreland basin"
		)
		userEvent.type(inputFields[3], '10.1130/g30177a.1')
		userEvent.type(
			inputFields[4],
			'https://pubs.geoscienceworld.org/gsa/geology/article-abstract/37/10/907/103864/Beyond-Beecher-s-Trilobite-Bed-Widespread'
		)
		userEvent.click(saveReferenceBtn)
		const firstAuthorLengthError = await screen.queryByText(
			'Ensure the author name is at most 50 characters',
			{ exact: false }
		)
		expect(firstAuthorLengthError).not.toBeInTheDocument()
		const yearError = await screen.queryByText(
			'Please provide correct year value'
		)
		expect(yearError).not.toBeInTheDocument()
		const missingTitleError = await screen.queryByText(
			'Please provide the title of the reference'
		)
		expect(missingTitleError).not.toBeInTheDocument()
		const titleLengthError = await screen.queryByText(
			'Ensure the title is at most 250 characters',
			{ exact: false }
		)
		expect(titleLengthError).not.toBeInTheDocument()
		const doiError = await screen.queryByText(
			'Enter the DOI number that begins with 10 followed by a period'
		)
		expect(doiError).not.toBeInTheDocument()
		const urlValidationError = await screen.queryByText(
			'Please enter correct url'
		)
		expect(urlValidationError).not.toBeInTheDocument()
		const urlLengthError = await screen.queryByText(
			'Ensure the url is at most 200 characters',
			{ exact: false }
		)
		expect(urlLengthError).not.toBeInTheDocument()
	})

	test('prints correct error if title is missing', async () => {
		const saveReferenceBtn = screen.getByRole('button')
		userEvent.click(saveReferenceBtn)
		const missingTitleError = await screen.findByText(
			'Please provide the title of the reference'
		)
		expect(missingTitleError).toBeInTheDocument()
	})

	test('prints correct error if title is more than 250 characters long', async () => {
		const inputFields = screen.getAllByRole('textbox')
		const saveReferenceBtn = screen.getByRole('button')
		userEvent.type(
			inputFields[2],
			"Beyond Beecher's Trilobite Bed: Widespread pyritization of soft tissues in the Late Ordovician Taconic foreland basin.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
		)
		userEvent.click(saveReferenceBtn)
		const titleLengthError = await screen.findByText(
			'Ensure the title is at most 250 characters (title has 251 characters)'
		)
		expect(titleLengthError).toBeInTheDocument()
	})

	test('prints correct error if author name is more than 50 characters long', async () => {
		const inputFields = screen.getAllByRole('textbox')
		userEvent.type(
			inputFields[0],
			'Úna C. Farrellaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
		)
		const saveReferenceBtn = screen.getByRole('button')
		userEvent.click(saveReferenceBtn)
		const firstAuthorLengthError = await screen.findByText(
			'Ensure the author name is at most 50 characters (name has 51 characters)'
		)
		expect(firstAuthorLengthError).toBeInTheDocument()
	})

	test('prints correct error if provided year is invalid', async () => {
		const inputFields = screen.getAllByRole('textbox')
		userEvent.type(inputFields[1], '1799')
		const saveReferenceBtn = screen.getByRole('button')
		userEvent.click(saveReferenceBtn)
		const yearError = await screen.findByText(
			'Please provide correct year value'
		)
		expect(yearError).toBeInTheDocument()
	})

	test('prints correct error if provided doi number is invalid', async () => {
		const inputFields = screen.getAllByRole('textbox')
		userEvent.type(inputFields[3], '10.0')
		const saveReferenceBtn = screen.getByRole('button')
		userEvent.click(saveReferenceBtn)
		const doiError = await screen.findByText(
			'Enter the DOI number that begins with 10 followed by a period'
		)
		expect(doiError).toBeInTheDocument()
	})

	test('prints correct error if provided link is invalid', async () => {
		const inputFields = screen.getAllByRole('textbox')
		userEvent.type(inputFields[4], 'javascript:alert("hello")')
		const saveReferenceBtn = screen.getByRole('button')
		userEvent.click(saveReferenceBtn)
		const urlValidationError = await screen.findByText(
			'Please enter correct url'
		)
		expect(urlValidationError).toBeInTheDocument()
	})

	test('prints correct error if provided link is more than 200 characters long', async () => {
		const inputFields = screen.getAllByRole('textbox')
		userEvent.type(
			inputFields[4],
			'http://www.somesite.com/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
		)
		const saveReferenceBtn = screen.getByRole('button')
		userEvent.click(saveReferenceBtn)
		const urlLengthError = await screen.findByText(
			'Ensure the url is at most 200 characters (url has 201 characters)'
		)
		expect(urlLengthError).toBeInTheDocument()
	})
})

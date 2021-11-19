import React from 'react'
import { expect, test, beforeEach, describe } from '@jest/globals'
import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import { DoiForm } from '../DoiForm'

const doi = '10.0'
const setQueried = () => {}
const setFirstAuthor = () => {}
const setYear = () => {}
const setTitle = () => {}
const setDoi = () => {}
const setLink = () => {}

describe('When reference form set to visible', () => {
	const displayRefForm = 'block'

	beforeEach(() => {
		render(
			<DoiForm
				{...{
					doi,
					setQueried,
					setFirstAuthor,
					setYear,
					setTitle,
					setDoi,
					setLink,
					displayRefForm,
				}}
			/>
		)
	})

	test('rendered doi form has two buttons', () => {
		expect(screen.getAllByRole('button')).toHaveLength(2)
	})

	test('rendered doi form has input field', () => {
		expect(screen.getByRole('textbox')).toBeInTheDocument()
	})
})

describe('When reference form set to invisible', () => {
	const displayRefForm = 'none'

	beforeEach(() => {
		render(
			<DoiForm
				{...{
					doi,
					setQueried,
					setFirstAuthor,
					setYear,
					setTitle,
					setDoi,
					setLink,
					displayRefForm,
				}}
			/>
		)
	})

	test('doi input field not visible', () => {
		expect(screen.queryByRole('textbox')).toBeNull()
	})
})

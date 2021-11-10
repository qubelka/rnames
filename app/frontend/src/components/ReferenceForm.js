import React, { useState, useEffect } from 'react'
import { useDispatch } from 'react-redux'
import { addRef, deleteRef, updateRef } from '../store/references/actions'
import { makeId } from '../utilities'
import { referenceFormIsValid } from '../validations'
import { InputField } from './InputField'

export const ReferenceForm = ({
	displayRefForm,
	showNewReferenceForm,
	reference = undefined,
	isQueried = false,
}) => {
	const dispatch = useDispatch()

	const [firstAuthor, setFirstAuthor] = useState('')
	const [year, setYear] = useState('')
	const [title, setTitle] = useState('')
	const [doi, setDoi] = useState('')
	const [link, setLink] = useState('')
	const [exists, setExists] = useState(false)
	const [queried, setQueried] = useState(isQueried)
	const [formFieldNotification, setFormFieldNotification] = useState({
		firstAuthor: null,
		year: null,
		title: null,
		doi: null,
		link: null,
	})
	const [showError, setShowErrors] = useState(false)

	useEffect(() => {
		if (!reference) return
		setFirstAuthor(reference.firstAuthor)
		setYear(reference.year)
		setTitle(reference.title)
		setDoi(reference.doi)
		setLink(reference.link)
		setExists(reference.exists)
	}, [])

	useEffect(() => {
		const refFormTimeoutId = setTimeout(() => {
			setFormFieldNotification({
				firstAuthor: null,
				year: null,
				title: null,
				doi: null,
				link: null,
			})
		}, 7000)
		return () => {
			clearTimeout(refFormTimeoutId)
		}
	}, [showError])

	const addErrorMessage = (message, field, type = 'error') => {
		setFormFieldNotification(prev => {
			return {
				...prev,
				[field]: { message, type },
			}
		})
	}

	const showErrorMsgs = () => {
		setShowErrors(!showError)
	}

	/* 	const doiSubmit = async e => {
		e.preventDefault()
		if (!doiFormIsValid(doi)) return

		try {
			const result = await axios.get(
				`https://api.crossref.org/works/${doi}`
			)
			const response = JSON.parse(result.request.response).message

			if (response.author.length === 0) return

			setQueried(true)
			setFirstAuthor(
				`${response.author[0].given} ${response.author[0].family}`
			)
			setYear(response.created['date-parts'][0][0])
			setTitle(response.title[0])
			setDoi(response.DOI)
			setLink(response.URL)
		} catch (err) {
			notify(`No resources found with ${doi}`)
		}
	} */

	const clearFields = () => {
		setFirstAuthor('')
		setYear('')
		setTitle('')
		setDoi('')
		setLink('')
		setExists(false)
		setQueried(false)
	}

	const handleNewDoiSearch = () => {
		clearFields()
		dispatch(deleteRef(reference))
	}

	const handleManualSubmit = e => {
		e.preventDefault()
		const valid = referenceFormIsValid(
			firstAuthor,
			year,
			title,
			doi,
			link,
			addErrorMessage
		)

		if (!valid) {
			showErrorMsgs()
			return
		}

		const newReference = {
			firstAuthor,
			year,
			title,
			doi,
			link,
			exists,
			queried,
			edit: false,
		}

		if (!reference) {
			dispatch(addRef({ ...newReference, id: makeId('reference') }))
		} else {
			dispatch(updateRef({ ...newReference, id: reference.id }))
		}

		clearFields()
		showNewReferenceForm()
	}

	if (queried)
		return (
			<div>
				<form onSubmit={handleManualSubmit}>
					<label htmlFor='first_author'>first_author</label>
					<InputField
						name='first_author'
						value={firstAuthor}
						setField={setFirstAuthor}
						notification={formFieldNotification.firstAuthor}
					/>
					<InputField
						name='year'
						value={year}
						setField={setYear}
						notification={formFieldNotification.year}
					/>
					<InputField
						name='title'
						value={title}
						setField={setTitle}
						notification={formFieldNotification.title}
					/>
					<InputField
						name='doi'
						value={doi}
						setField={setDoi}
						notification={formFieldNotification.doi}
					/>
					<InputField
						name='link'
						value={link}
						setField={setLink}
						notification={formFieldNotification.link}
					/>
					<button type='submit'>Save reference</button>
					{reference ? (
						<>
							<br />
							<button type='button' onClick={handleNewDoiSearch}>
								Make new doi search
							</button>
						</>
					) : (
						''
					)}
				</form>
			</div>
		)

	return (
		<>
			<form style={{ display: displayRefForm }}>
				<label htmlFor='doi'>doi</label>
				<input
					type='text'
					name='doi'
					value={doi}
					onChange={e => setDoi(e.target.value)}
				/>
				<button type='submit'>get</button>
				<button type='button' onClick={() => setQueried(true)}>
					Manual Entry
				</button>
			</form>
		</>
	)
}

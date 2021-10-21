import React from 'react'
import { useDispatch } from 'react-redux'
import axios from 'axios'
import { updateRef } from '../store/references/actions'
import { NameList } from './NameList'

export const Reference = ({ data }) => {
	const dispatch = useDispatch()

	const doiSubmit = async e => {
		e.preventDefault()
		const doi = e.target.doi.value
		try {
			const result = await axios.get(
				`https://api.crossref.org/works/${doi}`
			)
			const response = JSON.parse(result.request.response).message

			if (response.author.length === 0) return

			dispatch(
				updateRef({
					...data,
					queried: true,
					first_author: `${response.author[0].given} ${response.author[0].family}`,
					year: response.created['date-parts'][0][0],
					title: response.title[0],
					doi: response.DOI,
					link: response.URL,
				})
			)
		} catch (err) {
			// Do something with this later
			console.log(err.response.data)
		}
	}

	const update = ({ target }, field) => {
		const r = { ...data }
		r[field] = target.value
		dispatch(updateRef(r))
	}

	if (data.queried)
		return (
			<div>
				<form>
					<label htmlFor='first_author'>first_author</label>
					<input
						type='text'
						name='first_author'
						value={data.first_author}
						onChange={e => update(e, 'first_author')}
					/>
					<br />
					<label htmlFor='year'>year</label>
					<input
						type='text'
						name='year'
						value={data.year}
						onChange={e => update(e, 'year')}
					/>
					<br />
					<label htmlFor='title'>title</label>
					<input
						type='text'
						name='title'
						value={data.title}
						onChange={e => update(e, 'title')}
					/>
					<br />
					<label htmlFor='doi'>doi</label>
					<input
						type='text'
						name='doi'
						value={data.doi}
						onChange={e => update(e, 'doi')}
					/>
					<br />
					<label htmlFor='link'>link</label>
					<input
						type='text'
						name='link'
						value={data.link}
						onChange={e => update(e, 'link')}
					/>
				</form>
				<NameList {...{ data }} />
			</div>
		)

	return (
		<div>
			<form onSubmit={doiSubmit}>
				<label htmlFor='doi'>doi</label>
				<input
					type='text'
					name='doi'
					value={data.doi}
					onChange={e => update(e, 'doi')}
				/>
				<button type='submit'>get</button>
				<button
					type='button'
					onClick={() => {
						dispatch(updateRef({ ...data, queried: true }))
					}}
				>
					Manual Entry
				</button>
			</form>
		</div>
	)
}

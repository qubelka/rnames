import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import {
	selectStructuredName,
	deselectStructuredName,
} from '../store/selected_structured_names/actions'
import { loadServerData } from '../services/server'
import { formatStructuredName, parseId } from '../utilities'

export const SelectedStructuredNames = () => {
	const selection = useSelector(state => {
		return state.selectedStructuredNames
			.filter(v => parseId(v).type !== 'structured_name')
			.map(v => {
				return {
					id: v,
					formattedName: formatStructuredName(state.map[v], state),
				}
			})
	})

	const [search, setSearch] = useState('')
	const dbNames = loadServerData('structured_names') || []
	const dispatch = useDispatch()
	const dataListId = 'selectedStructuredNamesDataList'

	const handleChange = e => {
		const result = dbNames.find(v => e.target.value === v.formattedName)
		if (result) {
			setSearch('')
			dispatch(selectStructuredName(result.id))
		} else {
			setSearch(e.target.value)
		}
	}

	const handleDelete = id => dispatch(deselectStructuredName(id))

	return (
		<>
			<h2>Selected existing structured names</h2>
			{selection.map(v => (
				<>
					<button onClick={() => handleDelete(v.id)}>Delete</button>
					<span key={v.id}>{v.formattedName}</span>
					<br />
				</>
			))}

			<label>Select existing name</label>
			<input list={dataListId} value={search} onChange={handleChange} />
			<datalist id={dataListId}>
				{dbNames.map(v => (
					<option key={v.id}>{v.formattedName}</option>
				))}
			</datalist>
		</>
	)
}

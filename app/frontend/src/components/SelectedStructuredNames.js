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
	const relations = useSelector(v => v.rel)
	const [search, setSearch] = useState('')
	const dbNames = loadServerData('structured_names') || []
	const dispatch = useDispatch()
	const dataListId = 'selectedStructuredNamesDataList'

	const handleChange = e => {
		const selectedIdNumber = Number(e.target.value)
		const result = dbNames.find(v => selectedIdNumber === parseId(v.id).value)
		if (result) {
			setSearch('')
			dispatch(selectStructuredName(result.id))
		} else {
			setSearch(e.target.value)
		}
	}

	const handleDelete = id => {
		if (!relations.find(v => v.name1 === id || v.name2 === id))
			dispatch(deselectStructuredName(id))
	}

	return (
		<>
			<label>Select existing name</label>
			<input list={dataListId} value={search} onChange={handleChange} />
			<datalist id={dataListId}>
				{dbNames.map(v => (
					<option key={v.id} value={parseId(v.id).value}>{v.formattedName}</option>
				))}
			</datalist>
			{selection.map(v => (
				<div key={v.id}>
					<button onClick={() => handleDelete(v.id)}>Deselect</button>
					<span>{v.formattedName}</span>
				</div>
			))}
		</>
	)
}

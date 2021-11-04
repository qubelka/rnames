import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { parseId, makeId } from '../utilities'
import { addName } from '../store/names/actions'
import { addSname } from '../store/snames/actions'
import { Datalist } from './Datalist'
import {
	selectAllLocations,
	selectAllNames,
	selectMap,
	selectRefence,
} from '../store/snames/selectors'
import { selectStructuredName } from '../store/selected_structured_names/actions'

export const SnameForm = ({
	displaySnameForm,
	showNewSnameForm,
	newSnameButtonIsDisabled,
	setNewSnameButtonIsDisabled,
}) => {
	const dispatch = useDispatch()
	const reference = useSelector(selectRefence)
	const [name, setName] = useState('')
	const [location, setLocation] = useState('')
	const [qualifier, setQualifier] = useState('')

	const map = useSelector(selectMap)
	const names = useSelector(selectAllNames)

	const qualifiers = useSelector(v => {
		return Object.entries(v.map)
			.filter(([key]) => parseId(key).type === 'db_qualifier')
			.map(v => [v[1].id, map[v[1].qualifier_name_id].name])
	})

	const locations = useSelector(selectAllLocations)

	const handleSnameAddition = () => {
		if (!reference) {
			// Add error message later!
			console.log('Enter reference first!')
			return
		}

		const qualifierFromDb = qualifiers.find(
			dbQualifier => dbQualifier[1] === qualifier
		)

		// Add error message later!
		if (!qualifierFromDb) return

		let nameId, locationId
		if (!names.find(v => v[1] === name)) {
			nameId = makeId('name')
			dispatch(addName({ id: nameId, name: name, variant: 'name' }))
		}

		if (!locations.find(v => v[1] === location)) {
			locationId = makeId('location')
			dispatch(
				addName({ id: locationId, name: location, variant: 'location' })
			)
		}

		const newSname = {
			id: makeId('structured_name'),
			name_id: nameId || names.find(dbName => dbName[1] === name)[0],
			location_id:
				locationId ||
				locations.find(dbLocation => dbLocation[1] === location)[0],
			qualifier_id: qualifierFromDb[0],
			reference_id: reference.id,
			remarks: '',
		}
		dispatch(addSname(newSname))
		dispatch(selectStructuredName(newSname.id))
		setName('')
		setQualifier('')
		setLocation('')
		showNewSnameForm()
		setNewSnameButtonIsDisabled(!newSnameButtonIsDisabled)
	}

	return (
		<div style={{ display: displaySnameForm }}>
			<label htmlFor='name'>Name</label>
			<Datalist
				name='name'
				options={names}
				value={name}
				onChange={e => setName(e.target.value)}
			/>
			<br />
			<label htmlFor='qualifier'>Qualifier</label>
			<Datalist
				name='qualifier'
				options={qualifiers}
				value={qualifier}
				onChange={e => setQualifier(e.target.value)}
			/>
			<br />
			<label htmlFor='location'>Location</label>
			<Datalist
				name='location'
				options={locations}
				value={location}
				onChange={e => setLocation(e.target.value)}
			/>
			<br />
			<button type='button' onClick={handleSnameAddition}>
				Save
			</button>
		</div>
	)
}

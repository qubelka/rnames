import React from 'react'
import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { loadServerData, initServer } from './services/server'
import { makeId } from './utilities'
import { initMapvalues } from './store/map/actions'
import { addRef } from './store/references/actions'
import { addRel } from './store/relations/actions'
import { addSname } from './store/snames/actions'
import { Reference } from './components/Reference'
import { Sname } from './components/Sname'
import { Relation } from './components/Relation'
import { ReferenceForm } from './components/ReferenceForm'

const blankRef = () => {
	return {
		id: makeId('reference'),
		first_author: '',
		year: 0,
		title: '',
		doi: '',
		link: '',
		exists: false,
		queried: false,
		names: [],
	}
}
const blankSname = () => {
	return {
		id: makeId('structured_name'),
		name_id: -1,
		qualifier_id: -1,
		location_id: -1,
		reference_id: -1,
		remarks: '',
	}
}
const blankRel = () => {
	return { id: makeId('relation'), name1: -1, name2: -1, reference_id: -1 }
}

const App = () => {
	const state = useSelector(v => v)
	const dispatch = useDispatch()
	useEffect(() => {
		initServer()
		const serverData = loadServerData()
		const map = {}
		serverData.names.forEach(v => (map[v.id] = v))
		serverData.locations.forEach(v => (map[v.id] = v))
		serverData.qualifier_names.forEach(v => (map[v.id] = v))
		serverData.qualifiers.forEach(v => (map[v.id] = v))
		serverData.structured_names.forEach(v => (map[v.id] = v))
		serverData.references.forEach(v => (map[v.id] = v))
		dispatch(initMapvalues(map))
	}, [])

	const addNewRef = e => {
		const ref = blankRef()
		dispatch(addRef(ref))
	}

	const addSnameHandler = e => {
		const sname = blankSname()
		dispatch(addSname(sname))
	}

	const addRelHandler = e => {
		dispatch(addRel(blankRel()))
	}

	return (
		<>
			<div>
				<h2>References</h2>
				{state.ref.map(data => (
					<Reference {...{ key: data.id, data }} />
				))}
				<ReferenceForm />
				<button type='button' onClick={addNewRef}>
					Add new reference
				</button>
			</div>
			<div>
				<h2>Structured Names</h2>
				{state.sname.map(data => (
					<Sname {...{ key: data.id, data }} />
				))}
				<button type='button' onClick={addSnameHandler}>
					Add new structured name
				</button>
			</div>
			<div>
				<h2>Relations</h2>
				{state.rel.map(data => (
					<Relation {...{ key: data.id, data }} />
				))}
				<button type='button' onClick={addRelHandler}>
					Add new relation
				</button>
			</div>
		</>
	)
}

export default App

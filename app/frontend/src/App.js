import React from 'react'
import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import axios from 'axios'

import store, {addRef, updateRef, getId, parseId, addSname, updateSname, addRel, updateRel} from './store.js'

const Dropdown = ({name, options, value, onChange}) => {
	return(
		<select name= {name} onChange={onChange} value={value}>
			<option></option>
			{ options.map(tuple => <option key={tuple[0]} value={tuple[0]}>{tuple[1]}</option> )}
		</select>
	)
}

const NameEntry = ({id, data}) => {
	const dispatch = useDispatch()
	const name = data.names.find(v => v.id === id)

	const update = ({target}, field) => {
		const temp = {...name}
		temp[field] = target.value
		dispatch(updateRef({
			...data,
			names: data.names.map(v => v.id === id ? temp : v)
		}))
	}

	const updatevariant = newVariant => {
		const value = parseId(id).value
		const temp = {...name, id: getId(newVariant, value), variant: newVariant}
		dispatch(updateRef({
			...data,
			names: data.names.map(v => v.id === id ? temp : v)
		}))
	}

	const qualifierOptions = [
		[`bio`, `Biostratigraphy`],
		[`chemo`, `Chemostratigraphy`],
		[`chrono`, `Chronostratigraphy`],
		[`litho`,`Lithostratigraphy`],
		[`region`, `Regional Standard`],
		[`seq`, `Sequence-stratigraphy`]
	]

	const levelOptions = [
		[1, `1`],
		[2, `2`],
		[3, `3`],
		[4, `4`],
		[5, `5`],
		[6, `6`],
		[7, `7`]
	]

	const variantOptions = [
		[`name`, `Name`],
		[`location`, `Location`],
		[`qualifier`, `Qualifier`]
	]

	return (
		<div>
			<input type="text" name="name" value={name.name} onChange={e => update(e, `name`)} />
			<label htmlFor="variant">Type:</label>
			<Dropdown name="variant" onChange={e => updatevariant(e.target.value)} options={variantOptions} value={name.variant} />
			{ name.variant === `qualifier`
				?<>
				<label htmlFor="qualifier">Qualifier Name:</label>
				<Dropdown name="qualifier" onChange={e => update(e, `qualifier`)} options={qualifierOptions} value={name.qualifier} />
				<label htmlFor="level">Level:</label>
				<Dropdown name="level" onChange={e => update(e, `level`)} options={levelOptions} value={name.level} />
				</>
				: <></> }
		</div>
	)
}

const NameList = ({data}) => {
	const dispatch = useDispatch()
	const addNew = e => {
		dispatch(updateRef({
			...data,
			names: data.names.concat({id: getId(`name`), name: ``, variant: `name`, qualifier: `bio`, level: 1})
		}))
	}

	return (
		<div>
			{data.names.map(v => <NameEntry {...{key: v.id, id: v.id, data}} />)}
			<button type="button" onClick={addNew}>Add new name</button>
		</div>
	)
}

const Ref = ({data}) => {
	const dispatch = useDispatch()

	const doiSubmit = async e => {
		e.preventDefault()
		const doi = e.target.doi.value
		const result = await axios.get(`https://api.crossref.org/works/${doi}`)
		const response = JSON.parse(result.request.response).message

		if (!response.author)
			return

		dispatch(updateRef({
			...data,
			queried: true,
			author: `${response.author[0].given} ${response.author[0].family}`,
			year: response.created["date-parts"][0][0],
			title: response.title,
			doi: response.DOI,
			link: response.URL
		}))
	}

	if (data.queried)
		return (
			<div>
				<form>
					<label htmlFor="author">author</label>
					<input type="text" name="author" value={data.author} />
					<br />
					<label htmlFor="year">year</label>
					<input type="text" name="year" value={data.year} />
					<br />
					<label htmlFor="title">title</label>
					<input type="text" name="title" value={data.title} />
					<br />
					<label htmlFor="doi">doi</label>
					<input type="text" name="doi" value={data.doi} />
					<br />
					<label htmlFor="link">link</label>
					<input type="text" name="link" value={data.link} />
				</form>
				<NameList {...{data}} />
			</div>
		)

	return (
		<div>
			<form onSubmit={doiSubmit}>
				<label htmlFor="doi">doi</label>
				<input type="text" name="doi" />
				<button type="submit">get</button>
				<button type="button" onClick={() => {dispatch(updateRef({...data, queried: true}))}}>Manual Entry</button>
			</form>
		</div>
	)
}

const findRef = (refs, ids) => refs.find(ref => ref.names.find(v => ids.includes(v.id)))
const findId = (state, id) => {
	return state.ref.find(v => v.id === id)
		|| state.sname.find(v => v.id === id)
		|| state.rel.find(v => v.id === id)
		|| state.ref.reduce((p, c) => p.concat(...c.names), []).find(v => v.id === id)
}

const Sname = ({data}) => {
	const dispatch = useDispatch()
	const refData = useSelector(v => v.ref)
	const refs = refData.reduce((p, c) => p.concat(...c.names.map(v => {return {...v, refId: c.id}})), [])
	const names = refs.filter(v => v.variant === `name`)
	const qualifiers = refs.filter(v => v.variant === `qualifier`)
	const locs = refs.filter(v => v.variant === `location`)


	const nameOptions = names.map(v => [v.id, v.name])

	const qualifierOptions = qualifiers.map(v => [v.id, `${v.name} (${v.qualifier}) level ${v.level} `])

	const locationOptions = locs.map(v => [v.id, v.name])

	const update = ({target}, field) => {
		const r = {...data}
		r[field] = target.value
		const ref = findRef(refData, [r.name, r.qualifier, r.location])
		r.ref = ref === undefined ? `` : ref.id
		dispatch(updateSname(r))
	}

	const refOptions = refData.map(v => [v.id, v.title])

	return (<div>
		<label htmlFor="name">Name</label>
		<Dropdown name="name"  options={nameOptions} value={data.name} onChange={e => update(e, `name`)} />
		<label htmlFor="qualifier">Qualifier</label>
		<Dropdown name="qualifier"  options={qualifierOptions} value={data.qualifier} onChange={e => update(e, `qualifier`)} />
		<label htmlFor="location">Location</label>
		<Dropdown name="location" options={locationOptions} value = {data.location} onChange={e => update(e, `location`) } />
		<label htmlFor="reference">Reference</label>
		<Dropdown name="reference" options={refOptions} value = {data.ref} />
	</div>)
}

const Rel = ({data}) => {
	const dispatch = useDispatch()
	const state = useSelector(v => v)

	const refOptions = state.ref.map(v => [v.id, v.title])

	const update = ({target}, field) => {
		const r = {...data}
		r[field] = target.value
		const name1Ref = state.sname.find(v => v.id === r.name1) ? state.sname.find(v => v.id === r.name1).ref : -1
		const name2Ref = state.sname.find(v => v.id === r.name2) ? state.sname.find(v => v.id === r.name2).ref : -1

		const ref = state.ref.find(ref => ref.id === name1Ref || ref.id === name2Ref)
		r.ref = ref === undefined ? -1 : ref.id
		dispatch(updateRel(r))
	}

	const formatSnameOption = v =>
		`${findId(state, v.name) ? findId(state, v.name).name : `` } ${findId(state, v.qualifier) ? findId(state, v.qualifier).name : `` } ${findId(state, v.location) ? findId(state, v.location).name : ``}`

	const name1Options = state.sname.filter(v => v.id !== data.name2).map(v => [v.id, formatSnameOption(v)])
	const name2Options = state.sname.filter(v => v.id !== data.name1).map(v => [v.id, formatSnameOption(v)])

	return (<div>
		<Dropdown options={name1Options} value={data.name1} onChange={e => update(e, `name1`)} />
		<Dropdown options={name2Options} value={data.name2} onChange={e => update(e, `name2`)} />
		<label htmlFor="reference">Reference</label>
		<Dropdown name="reference" options={refOptions} value = {data.ref} />
	</div>)
}

const blankRef = () => { return {id: getId(`reference`), author: ``, year: 0, title: ``, doi: ``, link: ``, exists: false, queried: false, names: []}}
const blankSname = () => { return {id: getId(`structured_name`), name: -1, qualifier: -1, location: -1, ref: -1, remarks:`` }}
const blankRel = () => { return {id: getId(`relation`), name1: -1, name2: -1, ref: -1} }

const App = () => {
	const state = useSelector(v => v)
	const dispatch = useDispatch()

	useEffect(() => {
		// initialize data from server
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
				{ state.ref.map(data => <Ref {...{key: data.id, data}} />) }
				<button type="button" onClick={addNewRef}>Add new reference</button>
			</div>
			<div>
				<h2>Structured Names</h2>
				{ state.sname.map(data => <Sname {...{key: data.id, data}} />) }
				<button type="button" onClick={addSnameHandler}>Add new structured name</button>
			</div>
			<div>
				<h2>Relations</h2>
				{ state.rel.map(data => <Rel {...{key: data.id, data}} />) }
				<button type="button" onClick={addRelHandler}>Add new relation</button>
			</div>
		</>
	);
}

export default App
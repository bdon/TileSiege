var layer = protomaps.leafletLayer({url:'example.pmtiles'})
layer.addTo(map)

map.on('load', () => {
    fetch('samples.json').then(resp => {
        return resp.json()
    }).then(j => {
        let flyToRandom = () => {
            let idx = Math.floor(Math.random() * j.length)
            let sample = j[idx]
            map.flyTo([sample.lat,sample.lon],sample.zoom)
            setTimeout(flyToRandom,5000)
        }
        flyToRandom()
    })
})

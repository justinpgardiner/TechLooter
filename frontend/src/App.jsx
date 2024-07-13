import { useState } from 'react'
import './App.css'
import StoreCard from './components/StoreCard'

function App() {
  const imageLinks = ['./icons/bestbuy.png', './icons/microcenter.png', './icons/newegg.png', './icons/walmart.png', './icons/ebay.png']
  const [searchValue, setSearchValue] = useState('')
  const [capturedSearchValue, setCapturedSearchValue] = useState('')
  const [resultsTextVisible, setResultsTextVisible] = useState(false)
  const [resultsLoaded, setResultsLoaded] = useState(false)
  const [showResults, setShowResults] = useState(false)
  const [stores, setStores] = useState([])

  const getStoreData = async (search) => {
    console.log(search)
    let url = "http://127.0.0.1:5001/scrape?search=" + search;
    console.log(url)
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
      const json = await response.json();
      return json;
    } catch (error) {
      console.error(error.message);
    }
  }

  const handleKeydown = async (event) => {
    if (event.key == 'Enter'){
      setResultsTextVisible(true)
      setCapturedSearchValue(searchValue)
      setResultsLoaded(false)
      setShowResults(true)
      let storeData = await getStoreData(searchValue)
      let _stores = storeData.data.map((store, index) => {
        return new StoreInfo(store.store, imageLinks[index], store.products)
      })
      _stores = _stores.sort(function(a,b){
        let val1 = parseFloat(a.products[0].price.substring(a.products[0].price.indexOf("$") + 1, a.products[0].price.includes("to") ? a.products[0].price.indexOf(" ") : a.products[0].price.length).replace(",", ""))
        let val2 = parseFloat(b.products[0].price.substring(b.products[0].price.indexOf("$") + 1, b.products[0].price.includes("to") ? b.products[0].price.indexOf(" ") : b.products[0].price.length).replace(",", ""))
        let value = val1 - val2
      return value})
      setStores(_stores)
      setResultsLoaded(true)
    }
  }

  return (
    <>
      <div>
        <h1 id="title"><span id='tech'>tech</span><span id='looter'>Looter</span></h1>
        <h3 className="info">Search below to get competitive prices from top technology stores</h3>
        <input id='search-input' type='text'placeholder='search' value={searchValue} onChange={(event) => setSearchValue(event.target.value)} onKeyDown={handleKeydown}/>
      </div>
      <div className="results-container">
        {resultsTextVisible &&
        (<div id="results-text-container">
          <h2>{"Results For: " + capturedSearchValue}</h2>
          <h3><span className="info">Some results may be misleading, as they may represent monthly payments or be the price for a different product</span></h3>
          <div id="low-high-container">
            <div id="low-container"><h1 className="price-indicators"><span id="low-price">$</span></h1></div>
            <div id="high-container"><h1 className="price-indicators"><span id="high-price">$$$</span></h1></div>
          </div>
        </div>)}
        <div id="results-item-container">
          {
          (showResults && resultsLoaded) &&
            stores.map((store, index) => 
            <StoreCard  key={index}
                        store={store.store} 
                        imageLink={store.imageLink}
                        products={store.products}
            />
          )}
          {(showResults ? !resultsLoaded : resultsLoaded) &&// logical XOR
            <h2>Loading...</h2>
          }
        </div>
      </div>
    </>
  )
}

class StoreInfo{
  constructor(store, imageLink, products){
    this.store = store
    this.imageLink = imageLink
    this.products = products
  }
}

export default App

function StoreCard({key, store, imageLink, products}){
    return (
        <div key={key} className="card">
            <a href={products[0].link} target="_blank">
            <img src={imageLink} height='100' width='100'/>
            </a>
            <h3><b>{store}</b></h3>
            <a href={products[0].link} target="_blank">
            <h4>{products[0].title}</h4>
            </a>
            <h4><b>{products[0].price}</b></h4>
        </div>
    )
}

export default StoreCard
import Link from "next/link";

const Navbar = () => {
    return ( 
        <nav>
            <div className="logo">
                <h1><Link href="/" id="logo">Zia Apps</Link></h1>
            </div>
            <Link href="/">Home</Link>
            <Link href="/scan-receipt">Scan Receipt</Link>
            <Link href="/about">About</Link>
            <Link href="/contact">Contact</Link>
        </nav>
     );
}
 
export default Navbar;
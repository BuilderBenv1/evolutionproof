export default function App({ Component, pageProps }) {
  return (
    <>
      <style jsx global>{`
        * {
          box-sizing: border-box;
          margin: 0;
          padding: 0;
        }
        html, body {
          background: #0a0a0a;
          color: #e0e0e0;
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        a { color: inherit; }
      `}</style>
      <Component {...pageProps} />
    </>
  );
}

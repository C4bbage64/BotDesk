import speedtest

def run_speed_test():
    """
    Runs a speed test and returns the results.
    Returns:
        dict: {'download': float (Mbps), 'upload': float (Mbps), 'ping': float (ms)}
    """
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        
        # Threads=None defaults to multi-threading
        download_speed = st.download() / 1_000_000  # Convert bps to Mbps
        upload_speed = st.upload() / 1_000_000      # Convert bps to Mbps
        ping = st.results.ping
        
        return {
            "download": round(download_speed, 2),
            "upload": round(upload_speed, 2),
            "ping": round(ping, 2)
        }
    except Exception as e:
        raise Exception(f"Speed test failed: {str(e)}")

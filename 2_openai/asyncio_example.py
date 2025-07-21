import asyncio

async def fetch_data(id):
    """Simulate fetching data from a database or API"""
    await asyncio.sleep(1)  # Simulate network delay
    return f"Data for ID {id}"

async def process_data(data):
    """Simulate processing data"""
    await asyncio.sleep(0.5)  # Simulate processing time
    return f"Processed: {data}"

async def main():
    """Main function demonstrating asyncio usage"""
    print("Starting async operations...")
    
    # Create multiple tasks to run concurrently
    tasks = []
    for i in range(3):
        # Create task for fetching data
        fetch_task = asyncio.create_task(fetch_data(i))
        tasks.append(fetch_task)
    
    # Wait for all fetch operations to complete
    results = await asyncio.gather(*tasks)
    print(f"Fetched data: {results}")
    
    # Process the fetched data
    process_tasks = []
    for data in results:
        process_task = asyncio.create_task(process_data(data))
        process_tasks.append(process_task)
    
    # Wait for all processing to complete
    processed_results = await asyncio.gather(*process_tasks)
    print(f"Processed results: {processed_results}")
    
    print("All operations completed!")

# Example usage
if __name__ == "__main__":
    asyncio.run(main())

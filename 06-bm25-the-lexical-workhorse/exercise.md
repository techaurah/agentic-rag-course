# Exercise for Lesson 06: BM25

The sensitivity sweep says the knobs do not matter on this corpus. Test whether that survives a corpus change: restrict the index to plant care documents only (watering, pests, compost, seasonal calendar, plant care basics) and rerun the sweep on the golden questions whose gold documents are in that subset. Then write the two or three sentences you would put in a design doc: under what corpus conditions would you expect k1 and b to start mattering, and what measurement would you run before changing them on a production index of a million chunks?
